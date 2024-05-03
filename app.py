import configparser
import datetime
import os
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import fake_useragent
import pyautogui
from playsound import playsound
from time import sleep


PATH = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
config = configparser.ConfigParser()
config.read("settings.ini")

def play_sound(file_path):
    playsound(file_path)
def joinonlesson(browser):
    now = datetime.datetime.now()
    hours = now.hour
    lessons = {
        0 : [1, 2, 3, 4, 5, 6, 7],
        1 : [8, 9, 10, 11, 12, 13, 14, 15],
        2 : [16, 17, 18, 19, 20, 21, 22],
        3 : [23, 24, 25, 26, 27, 28, 29],
        4 : [30, 31, 32, 33, 34, 35, 36]
    }
    try:
        if hours == 8:
            numberoflesson = 0
        if hours == 9:
            numberoflesson = 1
        if hours == 10:
            numberoflesson = 2
        if hours == 11:
            numberoflesson = 3
        if hours == 12:
            numberoflesson = 4
        if hours == 13:
            numberoflesson = 5
        if hours == 14:
            numberoflesson = 6
        if hours == 15:
            numberoflesson = 7
    except:
        return
    if now.weekday() == 3:
        numberoflesson -= 1
    elif now.weekday() == 4:
        numberoflesson -= 1
    try:
        number = lessons[now.weekday()][numberoflesson]
    except KeyError:
        return
    sleep(2)
    uroki = browser.find_elements(By.CLASS_NAME, "calendar-event-subject")
    try:
        urok = 1
        for i in uroki:
            if urok == number:
                jointolessonhuman = ActionChains(browser).click(i)
                jointolessonhuman.perform()
                break
            urok += 1
    except Exception as e: 
        return
    try:                                                                     
        WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/ng-kit/dropdown/div/div/div[3]/div/ev-button/button'))
        ).click()
    except:
        return
    all_windows = browser.window_handles
    new_window = all_windows[-1]
    browser.switch_to.window(new_window)
    url = browser.current_url
    os.system(f'start {url}')
    if 'meet.google' in url:
        sleep(10)
        pyautogui.hotkey('f11')
        pyautogui.hotkey('ctrl', 'd')
        pyautogui.hotkey('ctrl', 'e')
        pyautogui.moveTo(1336, 517)
        pyautogui.click()
    else:
        sleep(10)
        pyautogui.moveTo(1005, 600)
        pyautogui.click()
    browser.close()
    browser.quit()



def login(username, parol):
    try:
        options = Options()
        options.add_argument(f'user-agent={fake_useragent.UserAgent}')
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")

        browser = webdriver.Chrome(options=options)

        browser.get('https://id.human.ua/auth/login')

        login = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-authorization/div/div[1]/div/app-login/div/div[4]/form/ng-input[1]/input'))
            )
        password = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-authorization/div/div[1]/div/app-login/div/div[4]/form/ng-input[2]/input'))
        )
        login.clear()
        login.send_keys(username)
        password.clear()
        password.send_keys(parol)
        browser.find_element(By.XPATH, '/html/body/app-root/app-authorization/div/div[1]/div/app-login/div/ev-button/button').click()
        WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-root/app-profile-root/div/app-profile/section/div/div[2]/app-wide-plates-groups/div/div/div[2]/div[5]'))
        ).click()
        WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-index/section/app-ui/div/ng-navigation/aside/div/div[4]/ul/li[2]/a/div[2]"))
        ).click()
        joinonlesson(browser)
    finally:
        browser.close()
        browser.quit()
        play_sound(f"{PATH}\\")
    return
email = 'None'
passw = 'None'
fullapp = True
def main():
    while True:
        try:
                data = config['CONFIG']
                email = data['email']
                passw = data['passw']
                now = datetime.datetime.now()
                hours = now.hour
                if 8 <= hours <= 15 and email != 'None' and passw != 'None':
                    if hours == 8:
                        login(email, passw)
                        sleep(((60 - now.minute) + 23)*60)
                    if (9 or 10 or 11 or 12) == hours:
                        login(email, passw)
                        sleep(((60 - now.minute) + 18)*60)
                    if hours == 13:
                        login(email, passw)
                        sleep(((60 - now.minute) + 13)*60)
                    if hours == 14:
                        login(email, passw)
                        sleep(((60 - now.minute) + 8)*60)
                    if hours == 15:
                        login(email, passw)
                        sleep(((60 - now.minute) + 60)*60)
                else:
                    sleep(1)
        except:
            sys.exit()