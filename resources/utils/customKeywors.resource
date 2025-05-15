*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Aguarda o elemente ficar Habilitado
    [Arguments]    ${localizador}
    [Timeout]    10s
    
    WHILE    ${True}
        ${status}    Run Keyword And Return Status       Element Should Be Enabled    ${localizador}
        Exit For Loop If      ${status}    
    END

Verifica e Clica
    [Arguments]    ${valor}
    Wait Until Element Is Visible    ${valor}
    Capture Page Screenshot
    Click Element   ${valor}

Verifica e Valida
    [Arguments]    ${verifica}    ${valida}
    Wait Until Element Is Visible    ${verifica}
    Capture Page Screenshot
    Element Text Should Be   ${verifica}   ${valida}
    #Capture Page Screenshot