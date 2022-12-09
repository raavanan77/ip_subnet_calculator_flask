*** Settings ***
Library  SeleniumLibrary
*** Variables ***
*** Test Cases ***
Testcase 1
    Open Browser    http://127.0.0.1:5000    chrome
    Input text    name:textinput    1.1.1.1/31
    Click Button    submit
    Check    '/html/body/div[3]/table[2]/tbody/tr[3]/td[3]'