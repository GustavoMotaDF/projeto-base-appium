*** Settings ***
Resource     ../../base.resource

*** Keywords ***
Seleciona o que você procura   
    [Arguments]     ${procuropor} 
   Verifica e Clica   ${oqueprocura.${PLATAFORMA}.procuropor.format(text='${procuropor}')}

    Aguarda o elemente ficar Habilitado    ${oqueprocura.btn_next}
    #Capture Page Screenshot
    Clique em Next  

Clica em Next
    Verifica e Clica    ${oqueprocura.btn_next}
    
    
