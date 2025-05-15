import yaml
import subprocess
import os
import time
import requests
from datetime import datetime
import threading
import json
import shutil

TEMPLATE_HTML = "template/index.html"
RESULTS_FOLDER = "results"
BASE_OUTPUT = "logs"
 # raiz onde o diretório de data será criado

# ─── Criação da estrutura de diretórios ──────────────────────────
dt_now = datetime.now()
date_folder = dt_now.strftime("%Y-%m-%d")
time_folder = dt_now.strftime("%H%M%S%f")[:-3]  # HHMMSSmmm

# Caminho final onde tudo será salvo
output_path = os.path.join(BASE_OUTPUT, date_folder, time_folder)
os.makedirs(output_path, exist_ok=True)


print(f"Estrutura criada em: {output_path}")

# ─── MONITORAMENTO ──────────────────────────────────────────────

def parse_stats_line(line):
    parts = line.split()
    name = parts[0]
    cpu = float(parts[1].replace('%', '').replace(',', '.'))
    mem = parts[2] + " " + parts[3]
    mem_usage = parts[2].replace('MiB', '').replace('GiB', '').replace(',', '.')
    try:
        mem_value = float(mem_usage)
        if 'GiB' in parts[2]:
            mem_value *= 1024
    except:
        mem_value = 0.0
    return name, cpu, mem_value

def monitor_containers(container_names, interval, output, stop_flag, output_dir):
    stats = {
        name: {
            "cpu": [],
            "mem": [],
            "start": datetime.now().isoformat()
        } for name in container_names
    }

    while not stop_flag["stop"]:
        cmd = ["docker", "stats", "--no-stream", "--format", "{{.Name}} {{.CPUPerc}} {{.MemUsage}}"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
        lines = result.stdout.strip().splitlines()

        for line in lines:
            try:
                name, cpu, mem = parse_stats_line(line)
                if name in stats:
                    stats[name]["cpu"].append(cpu)
                    stats[name]["mem"].append(mem)
            except Exception as e:
                print("Erro ao processar stats:", e)

        time.sleep(interval)

    for name in container_names:
        stats[name]["end"] = datetime.now().isoformat()
        stats[name]["mem_unit"] = "MiB"

        # Formatando CPU e memória
        stats[name]["cpu"] = [f"{v:.2f}%" for v in stats[name]["cpu"]]
        stats[name]["mem"] = [f"{int(v)} MiB" for v in stats[name]["mem"]]

        # Cálculo de min/max com segurança
        try:
            cpu_vals = [float(v.strip('%')) for v in stats[name]['cpu']]
            stats[name]["cpu_min"] = f"{min(cpu_vals):.2f}%" if cpu_vals else "0.00%"
            stats[name]["cpu_max"] = f"{max(cpu_vals):.2f}%" if cpu_vals else "0.00%"
        except:
            stats[name]["cpu_min"] = stats[name]["cpu_max"] = "0.00%"

        try:
            mem_vals = [int(v.split()[0]) for v in stats[name]['mem']]
            stats[name]["mem_min"] = f"{min(mem_vals)} MiB" if mem_vals else "0 MiB"
            stats[name]["mem_max"] = f"{max(mem_vals)} MiB" if mem_vals else "0 MiB"
        except:
            stats[name]["mem_min"] = stats[name]["mem_max"] = "0 MiB"

    output.update(stats)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for name, data in stats.items():
        filepath = os.path.join(output_dir, f"{timestamp}-{name}.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

# ─── APPIUM ─────────────────────────────────────────────────────

def is_appium_ready(remote_url):
    try:
        response = requests.get(f"{remote_url}/status", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def wait_all_appiums(devices, timeout=120):
    print("🌐 Verificando status do Appium para todos os devices...")
    start_time = time.time()
    pending = devices.copy()

    while time.time() - start_time < timeout:
        for device in pending[:]:
            if is_appium_ready(device["remote_url"]):
                print(f"✅ Appium disponível: {device['device_name']} ({device['remote_url']})")
                pending.remove(device)
            else:
                print(f"⏳ Aguardando Appium em {device['remote_url']}...")

        if not pending:
            return True

        time.sleep(5)

    print("❌ Timeout esperando Appium nos seguintes devices:")
    for device in pending:
        print(f" - {device['device_name']} ({device['remote_url']})")
    return False

# ─── EXECUÇÃO PRINCIPAL ─────────────────────────────────────────

with open("devices/devices.yml", "r") as f:
    config = yaml.safe_load(f)

devices = config["devices"]
argfiles_dir = "argfiles"
os.makedirs(argfiles_dir, exist_ok=True)

if not wait_all_appiums(devices, timeout=120):
    exit(1)

# Gera arquivos .args
for idx, device in enumerate(devices, start=1):
    argfile_path = os.path.join(argfiles_dir, f"device{idx}.args")
    with open(argfile_path, "w") as argfile:
        argfile.write(f"--variable REMOTE_URL:{device['remote_url']}\n")
        argfile.write(f"--variable DEVICE_NAME:{device['device_name']}\n")
        argfile.write(f"--variable UDID:{device['udid']}\n")
        argfile.write(f"--variable SYSTEM_PORT:{device['system_port']}\n")
        

# Configura e inicia o monitoramento
container_names = [device["device_name"] for device in devices]
monitor_data = {}
stop_flag = {"stop": False}
monitor_thread = threading.Thread(
    target=monitor_containers,
    args=(container_names, 5, monitor_data, stop_flag, output_path)
)
monitor_thread.start()

# Executa os testes com pabot
command = [
    "pabot",
    "--processes", str(len(devices)),
    "--outputdir", "results"
]
for i in range(1, len(devices) + 1):
    command.append(f"--argumentfile{i}")
    command.append(f"{argfiles_dir}/device{i}.args")
command.append("testes/")

print("🚀 Executando testes com o comando:")
print(" ".join(command))
subprocess.run(command)

# Finaliza o monitoramento
stop_flag["stop"] = True
monitor_thread.join()

print(f"\n✅ Monitoramento encerrado e dados salvos em: {output_path}")

# Gera manifest.json com os arquivos .json criados
json_files = [f for f in os.listdir(output_path) if f.endswith(".json")]
manifest_path = os.path.join(output_path, "manifest.json")
with open(manifest_path, "w") as f:
    json.dump(json_files, f, indent=2)

# Agora sim, copia o HTML e os resultados finais
shutil.copy(TEMPLATE_HTML, os.path.join(output_path, "index.html"))
shutil.copytree(RESULTS_FOLDER, os.path.join(output_path, "results"))

print("📁 Arquivos finais copiados com sucesso.")
