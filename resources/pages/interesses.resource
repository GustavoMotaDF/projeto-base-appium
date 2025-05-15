*** Settings ***
Resource     ../../base.resource
Library    Screenshot

*** Keywords ***
Clique em Next    
   Verifica e Clica    ${interesses.btn_next}
Seleciona interesses
    [Arguments]     @{nomeDoInteresse}

    FOR    ${valor}    IN    @{nomeDoInteresse}
       Verifica e Clica    ${interesses.${PLATAFORMA}.lista_de_itens.format(text='${valor}')}        
    END 
    
    Aguarda o elemente ficar Habilitado    ${interesses.btn_next}
    #Capture Page Screenshot
    Clique em Next   