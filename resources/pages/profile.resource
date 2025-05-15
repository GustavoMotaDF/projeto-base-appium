*** Settings ***
Resource        ../../base.resource

*** Keywords ***
Valida Titulo profile
   Verifica e Valida   ${profile.${PLATAFORMA}.titulo}   My Profile
 