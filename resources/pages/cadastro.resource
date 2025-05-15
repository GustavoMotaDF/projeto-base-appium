*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Pula Cadastro
    Verifica e Clica    ${cadastro.${PLATAFORMA}.pula}
    #Capture Page Screenshot
