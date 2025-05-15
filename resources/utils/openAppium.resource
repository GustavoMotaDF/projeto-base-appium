*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Open App
    [Arguments]    ${REMOTE_URL}    ${DEVICE_NAME}    ${UDID}    ${SYSTEM_PORT}
    Open Application
    ...    remote_url=${REMOTE_URL}
    ...    appium:deviceName=${DEVICE_NAME}
    ...    appium:udid=${UDID}
    ...    appium:systemPort=${SYSTEM_PORT}
    ...    appium:automationName=${AUTOMATION}
    ...    platformName=${PLATAFORMA}
    ...    appium:app=/apps/app.apk
    ...    appium:disableIdLocatorAutocompletion=${True}
    ...    appium:enforceAppInstall=false