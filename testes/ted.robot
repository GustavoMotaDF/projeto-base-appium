*** Settings ***
Resource        ../base.resource
Test Setup      Open App     ${REMOTE_URL}    ${DEVICE_NAME}    ${UDID}    ${SYSTEM_PORT}
Test Teardown   Close All Applications

*** Test Cases ***
Cenário: Acessar app ${DEVICE_NAME}
    #Clique em Cancel
    Clique Em Lets Go
    Seleciona interesses    Technology    Science
    Seleciona o que você procura    Professional growth
    Pula Cadastro
    Valida titulo Home
    Acessa profile
    Valida Titulo profile