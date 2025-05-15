*** Settings ***
Library     AppiumLibrary    timeout=30
    
Resource    resources/utils/openAppium.resource
Resource    resources/utils/customKeywors.resource

Resource    resources/pages/welcome.resource
Resource    resources/pages/interesses.resource
Resource    resources/pages/oqueProcura.resource
Resource    resources/pages/cadastro.resource
Resource    resources/pages/home.resource
Resource    resources/pages/profile.resource
Resource    resources/pages/menu.resource

Variables   resources/locators/welcomeLocators.yml
Variables   resources/locators/interesses.yml
Variables   resources/locators/oqueprocura.yml
Variables   resources/locators/cadastro.yml
Variables   resources/locators/home.yml
Variables   resources/locators/profile.yml
Variables   resources/locators/menu.yml

Variables    devices/devices.yml


*** Variables ***

${PLATAFORMA}     android
${AUTOMATION}     UIAutomator2
${DEVICE_NAME}    Unknown
${REMOTE_URL}     Unknown
${UDID}           Unknown
${SYSTEM_PORT}    Unknown
