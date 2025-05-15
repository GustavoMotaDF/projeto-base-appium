*** Settings ***
Resource        ../../base.resource

*** Keywords ***

Valida titulo Home
    Vá para Home
    Verifica e Valida   ${home.${PLATAFORMA}.titulo}    New on TED     
Acessa profile
    Verifica e Clica    ${home.${PLATAFORMA}.myprofile}