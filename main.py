from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.ui as UI
from selenium.common.exceptions import TimeoutException
from contextlib import contextmanager
from timeit import default_timer
from bs4 import BeautifulSoup as BS
import time
import random
import sys
import string
from termcolor import colored

@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

# Login information
login_name = ""
password_text = ""

# prep
current_stamina = 0
percent_stamina = 0

current_toxic = 0
percent_toxic = 0

error_counter = 0
rave_counter = 0

original_stdout = sys.stdout

power_dict = {
    "Robber": {
        "Prospect": 100,
        "Newbie": 100,
        "Snitch": 100,
        "Pickpocket": 100,
        "Shoplifter": 10000,
        "Crook": 40000,
        "Burglar": 75000,
        "Larcenist": 150000,
        "Mugger": 200000,
        "Kingpin": 300000,
        "Mobster": 450000,
        "Padrino": 600000,
        "Godfather": 3000000
    },
    "Hitman": {
        "Prospect": 100,
        "Bruiser": 100,
        "Bravo": 100,
        "Goon": 100,
        "Garrotter": 20000,
        "Cut-throat": 60000,
        "Murderer": 90000,
        "Butcher": 160000,
        "Desperado": 250000,
        "Kingpin": 450000,
        "Mobster": 500000,
        "Padrino": 900000,
        "Godfather": 3000000
    },
    "Businessman": {
        "Prospect": 100,
        "Ware-slave": 100,
        "Swindler": 100,
        "Employer": 100,
        "Entrepreneur": 10000,
        "Banker": 40000,
        "Manager": 75000,
        "Director": 150000,
        "Top executive": 200000,
        "Kingpin": 300000,
        "Mobster": 450000,
        "Padrino": 600000,
        "Godfather": 3000000
    },
    "Pimp": {
        "Prospect": 100,
        "Popcorn": 100,
        "Gigolo": 100,
        "Bawd": 100,
        "Pet Owner": 10000,
        "Player": 40000,
        "Procurer": 75000,
        "Pander": 150000,
        "Bitch Ruler": 200000,
        "Kingpin": 300000,
        "Mobster": 450000,
        "Padrino": 600000,
        "Godfather": 3000000
    },
    "Broker": {
        "Prospect": 100,
        "Hangaround": 100,
        "Criminal": 100,
        "Thug": 100,
        "Mafioso": 10000,
        "Capo": 40000,
        "Consigliere": 75000,
        "Boss": 150000,
        "Don": 200000,
        "Kingpin": 300000,
        "Mobster": 450000,
        "Padrino": 600000,
        "Godfather": 3000000
    },
    "Dealer": {
        "Prospect": 100,
        "Hangaround": 100,
        "Criminal": 100,
        "Thug": 100,
        "Mafioso": 10000,
        "Capo": 40000,
        "Consigliere": 75000,
        "Boss": 150000,
        "Don": 200000,
        "Kingpin": 300000,
        "Mobster": 450000,
        "Padrino": 600000,
        "Godfather": 3000000
    }

}

ignore_list = [ "Godfather", "Padrino", "Mobster", "Kingpin", "Don", "Top executive", "Bitch Ruler", "Mugger", "Cut-throat", "Murderer", "Butcher", "Desperado"]
name_ignore = [ "LanceHenriksen", "fraggerek", "Copat6"]

# patched cdc chromedriver
driver = webdriver.Chrome("chromedriver")
executor_url = driver.command_executor._url
session_id = driver.session_id

def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver

# Open site + login
def login():
    global driver, login_name, password_text
    driver.get("https://www.thecrims.com/")
    

    # write username to form
    username_input = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginform"]/input[1]')))
    if username_input:
        try:
            username_input = driver.find_element_by_xpath('//*[@id="loginform"]/input[1]')
            username_input.send_keys(f'{login_name}') 
        except Exception as e: 
            print(e)

    # write password to form
    password_input = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="loginform"]/input[2]')))
    if password_input:
        try:
            password_input = driver.find_element_by_xpath('//*[@id="loginform"]/input[2]')
            password_input.send_keys(f'{password_text}') 
        except Exception as e: 
            print(e)
    
    try:
        login_button = driver.find_element_by_xpath('//*[@id="loginform"]/button') 
        login_button.click()
    except Exception as e: print(e)

# Get stamina
def getStamina():
    global current_stamina, percent_stamina
    stamina_bar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nightclub-singleassault-attack-18"]/div')))
    if stamina_bar:
        current_stamina = driver.find_element_by_xpath('//*[@id="nightclub-singleassault-attack-18"]/div').value_of_css_property("width")
        percent_stamina = round(100*float(current_stamina[:-2])/128)

# Get addiction
def getAddiction():
    global current_toxic, percent_toxic
    toxic_bar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nightclub-singleassault-attack-19"]/div')))
    if toxic_bar:
        current_toxic = driver.find_element_by_xpath('//*[@id="nightclub-singleassault-attack-19"]/div').value_of_css_property("width")
        percent_toxic = round(100*float(current_toxic[:-2])/128)

def printStamina():
    global current_stamina, percent_stamina
    getStamina()
    print("[INFO] stamina - " + str(percent_stamina))

def printToxic():
    global current_toxic, percent_toxic
    getAddiction()
    print("[INFO] toxic - " + str(percent_toxic))

def goRobMenu():
    pass

def selectRob():
    pass

# Rob single
def robSingle():
    global percent_stamina, percent_toxic
    global driver
    getStamina()
    getAddiction()

    if int(percent_toxic) >= 2:
        detox() 
        # detox
        
    if int(percent_stamina) < 100:
        refreshStamina()

        # //*[@id="menu-robbery"]
    
    robbery_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-robbery"]')))
    if robbery_button:
        robbery_button.click()
        robbery_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-robbery"]')))
        if robbery_button:
            robbery_button.click()
        
        select = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='singlerobbery-select-robbery']")))
        select = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='singlerobbery-select-robbery']/option[@value='8']")))
        if select:
            # selector = driver.find_element_by_xpath('//*[@id="singlerobbery-select-robbery"]')
            # all_options = selector.find_elements_by_tag_name("option")
            # for option in all_options:
            #     if "SP: 100%" in option.text:
            #         print("%s -> %s" % (option.get_attribute("value"), option.text.strip()), end="\n")
            selector = Select(driver.find_element_by_xpath('//*[@id="singlerobbery-select-robbery"]'))
            #selector.select_by_value('1')
            selector.select_by_value('48')

            #//*[@id="full"]
            checkbox_button = driver.find_element_by_xpath('//*[@id="full"]')
            #print(checkbox_button.is_selected())
            if checkbox_button.is_selected() == False:
                checkbox_button.click()

            # //*[@id="singlerobbery-rob"]
            # let's rob
            rob_button = driver.find_element_by_xpath('//*[@id="singlerobbery-rob"]')
            if rob_button:
                rob_button.click()
                time.sleep(1)

# detox
def detox():
    global percent_toxic
    global driver
    # //*[@id="menu-hospital"]
    hospital_button = driver.find_element_by_xpath('//*[@id="menu-hospital"]')
    if hospital_button:
        hospital_button.click()
        # metdaone
        # //*[@id="content_middle"]/div/div[3]/table[1]/tbody/tr[5]/td[4]/input
        # //*[@id="content_middle"]/div/div[3]/table[1]/tbody/tr[5]/td[4]/input
        metadone_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content_middle"]/div/div[3]/table[1]/tbody/tr[5]/td[4]/input')))
        if metadone_input:
            try:
                metadone_input = driver.find_element_by_xpath('//*[@id="content_middle"]/div/div[3]/table[1]/tbody/tr[5]/td[4]/input')
                metadone_input.send_keys(f'{percent_toxic}') 
            except Exception as e: 
                print(e)
            
            try:
                metadone_button = driver.find_element_by_xpath('//*[@id="content_middle"]/div/div[3]/table[1]/tbody/tr[5]/td[4]/button') 
                metadone_button.click()
            except Exception as e: print(e)

# Go to rave - get full stamina - get out
def refreshStamina():
    global driver
    global percent_stamina, percent_toxic
    # go to rave -> //*[@id="menu-nightlife"]
    rave_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-nightlife"]')))
    if rave_button:
        rave_button = driver.find_element_by_xpath('//*[@id="menu-nightlife"]')
        if rave_button:
            rave_button.click()

    # rave 1 //*[@id="content_middle"]/div/div[3]/div[3]/ul[4]/li[1]/div/div[2]/div[2]/button
    #        //*[@id="content_middle"]/div/div[3]/div[3]/ul[2]/li[1]/div/div[2]/div[2]/button
    #
    # rave 2 //*[@id="content_middle"]/div/div[3]/div[3]/ul[4]/li[2]/div/div[2]/div[2]/button
    
    # //*[@id="content_middle"]/div/div[3]/div[2]/table/tbody/tr[2]/td[5]/div/button
    # 
    rave_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content_middle"]/div/div[3]/div[2]/table/tbody/tr[1]/td[5]/div/button')))
    if rave_button:
        rave_button = driver.find_element_by_xpath('//*[@id="content_middle"]/div/div[3]/div[2]/table/tbody/tr[1]/td[5]/div/button')
        # //*[@id="content_middle"]/div/div[3]/div[2]/table/tbody/tr[1]/td[5]/div/button
        if rave_button:
            rave_button.click()
    
    # buy hooker stamina 
    # //*[@id="content_middle"]/div/div[3]/table[2]/tbody/tr/td[4]/button
    # //*[@id="nightclub-drug-buy-button-2957"]
    rave_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@id, "nightclub-drug-buy-button")]')))
    if rave_button:
        rave_button = driver.find_element_by_xpath('//*[starts-with(@id, "nightclub-drug-buy-button")]')
        if rave_button:
            rave_button.click()


    # leave rave -> 
    # //*[@id="exit-button-l5Jol5-ZaWnLl2-Wl3CYm5yTapdplWeVmGZlm2eanJmdmGaXnQ"]

    # //*[@id="exit-button-l5Jol5-ZaWnLl2-Wl3CYm5yTapdplWeVmGZlm2eanJmdmGaXnQ"]
    # //*[@id="exit-button-aWVtmm1mmJ7HaWdox5pox5-Ua2JmkmyXbGVlaWWXaJJva2uaaw"]
    # //*[@id="exit-button-aWVtmm1mmJ7HaWdox5pox5-Ua2JmkmyXbGVlaWWXaJJva2uaaw"]

    # //*[@id="exit-button-aGGalnGcapyZYmljyXCbmHFhbWZpmmucZWaWcWacnZNuZ5iWbw"]

    #rave_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="exit-button-l5Jol5-ZaWnLl2-Wl3CYm5yTapdplWeVmGZlm2eanJmdmGaXnQ"]')))
    rave_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@id, "exit-button")]')))
    if rave_button:
        #rave_button = driver.find_element_by_xpath('//*[@id="exit-button-l5Jol5-ZaWnLl2-Wl3CYm5yTapdplWeVmGZlm2eanJmdmGaXnQ"]')
        rave_button = driver.find_element_by_xpath('//*[starts-with(@id, "exit-button")]')
        #  //*[starts-with(@id, "exit-button")]
        if rave_button:
            rave_button.click()
            time.sleep(2)

    # //*[@id="exit-button-aWVtnG1omJyWa2FonJZjycucaWiWlnGaapNrYWZpk2draG2WZA"]
    # //*[@id="exit-button-aWVtnG1omJyWa2FonJZjycucaWiWlnGaapNrYWZpk2draG2WZA"]
    # //*[@id="exit-button-aWVtnG1omJyWa2FonJZjycucaWiWlnGaapNrYWZpk2draG2WZA"]


    # buy booze - //*[@id="nightclub-drug-buy-button-2415"]
    # //*[@id="nightclub-drug-buy-button-2415"]

def prepareHunt():
    # hunt info

    # get list of top killers

    # make list of dangerous classes

    # set target respect

    # save them globally
    pass 

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def scanVisitors():
    global driver, original_stdout
    global ignore_list
    # scan for players
    
    try:
        visitor_list = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[4]/div/table/tbody/tr/td[1]/div[2]/table/tbody/tr/td/div[2]/div/div[3]/div[1]/h3')))
        if visitor_list:
            #print("-> found visitors.")
            try:
                visitor_div = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div/table/tbody/tr/td[1]/div[2]/table/tbody/tr/td/div[2]/div/div[3]/div[1]')
                visitors = visitor_div.find_elements_by_xpath('.//*[starts-with(@class, "visitor-")]')
                for visitor in [visitors[0]]:
                    #log_name = 'logs/visitor_{}'.format(randomString(8))
                    #print(log_name)

                    #with open(log_name + "_details.html", 'w') as f:
                        #f.write(visitor.get_attribute('innerHTML'))
                        #print(visitor.get_attribute('innerHTML'))

                    # find stats
                    # name
                    # respect
                    # profession
                    # level
                    soup = BS(visitor.get_attribute('innerHTML'), 'html.parser')
                    visitor_name = ""
                    for div in soup.find_all('div', attrs={'class': 'user_list_username'}):
                        visitor_name = div.text.strip()
                    
                    first_children = [i.text for i in soup.select('.visitor_information div:last-child')]
                    #print(first_children)
                    #print(first_children[-1])
                    visitor_respect = first_children[-1].strip()
                    visitor_respect = visitor_respect.replace("Respect:", "").strip()
                    visitor_respect = int(visitor_respect)
                    # nth-last-child(2)
                    first_children = [i.text for i in soup.select('.visitor_information div:nth-last-child(2)')]
                    visitor_prof = first_children[0].strip()

                    first_children = [i.text for i in soup.select('.visitor_information div:nth-last-child(3)')]
                    visitor_rank = first_children[0].strip()

                    rank_text = ""
                    estimate_power = ""

                    print("{} : {} - {} - {} ".format(colored(visitor_name,"blue"), colored(f'{visitor_respect:,}', "green"), colored(visitor_prof, "yellow"), colored(visitor_rank, "magenta")))
                    # find boom box
                    # click choose
                    # nightclub-singleassault-select-open
                    try:
                        select_open = visitor.find_element_by_xpath('.//*[starts-with(@id, "nightclub-singleassault-select-open")]')
                        if select_open:
                            select_open.click()
                        

                        # click single
                        # nightclub-select-assault-type-single
                        type_single = visitor.find_element_by_xpath('.//*[starts-with(@id, "nightclub-select-assault-type-single")]')
                        if type_single:
                            type_single.click()

                        attack_him = False
                        if visitor_rank != "Hitman":
                            if visitor_name not in name_ignore:
                                if visitor_prof not in ignore_list:
                                    if visitor_respect <=160000:
                                            attack_him = True
                        else:
                            if visitor_respect <=70000:
                                attack_him = True

                        # click kill
                        # nightclub-attack
                        type_kill = visitor.find_element_by_xpath('.//*[starts-with(@id, "nightclub-attack")]')
                        if type_kill:
                            if attack_him:
                                type_kill.click()
                                leaveRave(sleep=1)
                                print("{} : {} - {} - {} ".format(colored(visitor_name,"red"), colored(f'{visitor_respect:,}', "green"), colored(visitor_prof, "yellow"), colored(visitor_rank, "magenta")))   
                                time.sleep(5)
                                return
                                #driver.quit()
                                #sys.exit(0)
                            else:
                                pass
                                #print("You are safe for now -> {} : {} - {} - {} ".format(colored(visitor_name,"red"), colored(f'{visitor_respect:,}', "green"), colored(visitor_prof, "yellow"), colored(visitor_rank, "magenta")))
                        leaveRave(sleep=1)
                    except:
                        leaveRave(sleep=1)
            except:
                leaveRave(sleep=2)
    except:
        pass

def scanPrey():
    global driver
    global percent_stamina, percent_toxic
    try:
        getStamina()
        if int(percent_stamina) < 50:
            refreshStamina()
        getAddiction()
        if int(percent_toxic) >= 5:
            detox() 
        enterRandomRave(sleep=0)
        scanVisitors()
        leaveRave(sleep=0)
    except:
        increaseErrorCount()

def increaseRaveCount():
    global rave_counter
    rave_counter += 1
    #print("[INFO] - Raves visited : {}".format(rave_counter))

def goDrinkBoze():
    pass

def goRaveMenu(sleep=2):
    global driver
    if sleep == -1:
        sleep = random.randint(2,5)
    time.sleep(sleep)
    try:
        rave_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-nightlife"]')))
        if rave_button:
            rave_button = driver.find_element_by_xpath('//*[@id="menu-nightlife"]')
            if rave_button:
                rave_button.click()
    except:
        increaseErrorCount()

def leaveRave(sleep=5):
    global rave_counter
    if sleep == -1:
        sleep = random.randint(3,7)
    global driver
    try:
        rave_button = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, '//*[starts-with(@id, "exit-button")]')))
        if rave_button:
            rave_button = driver.find_element_by_xpath('//*[starts-with(@id, "exit-button")]')
            if rave_button:
                rave_button.click()
                
        increaseRaveCount()
        time.sleep(sleep)
    except:
        increaseErrorCount()

def enterRandomRave(sleep=0):
    global driver
    if sleep == -1:
        sleep = random.randint(2,5)
    time.sleep(sleep)
    rave_number = random.randint(3, 10)
    xpath_rave = '(//button[contains(@class,"btn btn-inverse btn btn-inverse btn-small pull-right")])[{}]'.format(rave_number)
    try:
        rave_button = WebDriverWait(driver, 4).until(EC.visibility_of_element_located((By.XPATH, xpath_rave)))
        if rave_button:
            rave_button = driver.find_element_by_xpath(xpath_rave)
            if rave_button:
                rave_button.click()
    except:
        increaseErrorCount()

def checkErrorCount():
    global error_counter, driver
    # if error_counter == 50:
    #     print("[INFO] ABORTED DUE TO ERROR COUNT - {}".format(error_counter))
    #     leaveRave(sleep=0)
    #     driver.quit()
    #     sys.exit(1)

def increaseErrorCount():
    global error_counter
    error_counter += 1
    checkErrorCount()

def hunt():
    # hunt
    pass
    # go to rave menu

    # if stam < 50 - first thing when enter rave - drink fast

    # enter random disco with booze

    # scan for players

    # check for danger name or profession - rank
    # escape if danger


    # check respect

    # hit

    # leave rave

    # sleep random



if __name__ == "__main__":
    login()
    #robSingle()
    #time.sleep(20)
    time.sleep(5)
    while True:
        #robSingle()
        goRaveMenu(sleep=2)
        scanPrey()
