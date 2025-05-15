*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Vá para Home
    Verifica e Clica  ${menu.inferior.${PLATAFORMA}.home}  
Vá para Browse
    Verifica e Clica  ${menu.inferior.${PLATAFORMA}.browse}  
Vá para surpreenda-me
    Verifica e Clica  ${menu.inferior.${PLATAFORMA}.surpriseme}  
Vá para minha biblioteca
    Verifica e Clica  ${menu.inferior.${PLATAFORMA}.mylibrary}  
Vá para Podcasts
    Verifica e Clica  ${menu.inferior.${PLATAFORMA}.podcasts}  
