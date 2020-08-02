from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from difflib import SequenceMatcher
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from playsound import playsound

import time

# while True:
mon = 4
day = 1
oldDay = 0
#while True:

def startAppCheck():
    attempt = 0

    ##opening browser
    browser = webdriver.Firefox()
    browser.minimize_window()
    browser.get('https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm')


    ## filling the fields
    category = Select(browser.find_element_by_id('Category'))
    category.select_by_value('All')

    subCat = Select(browser.find_element_by_id('SubCategory'))
    subCat.select_by_value('All')

    gnibConf = Select(browser.find_element_by_id('ConfirmGNIB'))
    gnibConf.select_by_value('New')
    # gnibConf.select_by_value('Renewal')3

    # gnibno = browser.find_element_by_id('GNIBNo')
    # gnibno.send_keys('917252')
    #
    # gnibex_date = browser.find_element_by_id('GNIBExDT')
    # browser.execute_script("arguments[0].value = arguments[1]", gnibex_date, '01/09/2019')

    declare = browser.find_element_by_id('UsrDeclaration')
    declare.click()

    ## Enter your given name
    name = browser.find_element_by_id('GivenName')
    name.send_keys('<<GIVEN NAME>>')

    ## Enter your surname
    surname = browser.find_element_by_id('SurName')
    surname.send_keys('<<END NAME>>')

    ## Enter you DOB
    dob = browser.find_element_by_id('DOB')
    browser.execute_script("arguments[0].value = arguments[1]", dob, '<<DOB(DD/MM//YYYY)>>')

    ## Enter you nationality ( check from the list on the GNIB website )
    nation = browser.find_element_by_id('Nationality')
    browser.execute_script("arguments[0].value = arguments[1]", nation, '<<NATIONALITY>>')

    ## Enter your mail ID
    mail = browser.find_element_by_id('Email')
    mail.send_keys('<<EMAIL ID>>')

    ## Enter you mail ID
    confmail = browser.find_element_by_id('EmailConfirm')
    confmail.send_keys('<<EMAIL ID>>')

    fam = browser.find_element_by_id('FamAppYN')
    browser.execute_script("arguments[0].value = arguments[1]", fam, 'No')

    passpo = Select(browser.find_element_by_id('PPNoYN'))
    passpo.select_by_index(1)

    ## Enter your passport number
    ppN = browser.find_element_by_id('PPNo')
    ppN.send_keys('<<PASSPORT No. >>')

    ## ENTER PATH TO A SOUND FILE
    music_path = '<<SOUND FILE PATH>>'

    butt = browser.find_element_by_id('btLook4App')
    butt.click()

    date = Select(browser.find_element_by_id('AppSelectChoice'))
    #date.select_by_value('D')
    date.select_by_value('S')

    #slot = browser.find_element_by_id('btSrchByDT')
    slot = browser.find_element_by_id('btSrch4Apps')
    #appDate = browser.find_element_by_id('Appdate')

    while True:
        #date = str(day) + '/0' + str(mon) + '/2019'
        #browser.execute_script("arguments[0].value = arguments[1]", appDate, date)

        slot.click()
        time.sleep(2)
        delay = 3
        try:
            myElem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.XPATH, """//*[@id="dvAppOptions"]/table/tbody/tr/td[2]""")))

            #print(date + '- ' + myElem.text)
            #b = 'No appointment(s) available for that date'
            b = 'No appointment(s) are currently available'
            ratio = SequenceMatcher(None, myElem.text, b).ratio()
            if ratio == 1.0:
                print('nA - No appointment(s) are currently available -     ' + str(attempt))
            else:
                print('Got it !!!')

                ## ENTER A SOUND FILE
                playsound(music_path)
                time.sleep(10000)


        except TimeoutException:
            print('Timeout')
            playsound(music_path)
            ## Most of the appointments got here - can add a sleep
        except StaleElementReferenceException:
            print('Stale')
            playsound(music_path)

            myElem = WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, """//*[@id="dvAppOptions"]/table/tbody/tr/td[2]""")))

            # print(date + '- ' + myElem.text)
            #b = 'No appointment(s) available for that date'
            b = 'No appointment(s) are currently available'
            ratio = SequenceMatcher(None, myElem.text, b).ratio()
            if ratio == 1.0:
                print('No appointment(s) are currently available')
            else:
                print('Got it !!!')
                playsound(music_path)
                time.sleep(10000)

        attempt = attempt + 1
        if(attempt > 50):
            browser.close()
            startAppCheck()

startAppCheck()
