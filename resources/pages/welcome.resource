*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Clique em Cancel
    Verifica e Clica    ${welcome.${PLATAFORMA}.btn_cancel}
Clique Em Lets Go
    #Capture Page Screenshot
    Verifica e Clica    ${welcome.btn_next}
    
