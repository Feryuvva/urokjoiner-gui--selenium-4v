import flet as ft
import threading
import asyncio
import sys
import os
import configparser
import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import fake_useragent
import pyautogui
from time import sleep

import configparser

# Получаем путь к включенным файлам
PATH = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
config = configparser.ConfigParser()
config.read("settings.ini")

EXE_PATH = os.path.abspath(sys.argv[0])

# Получаем путь к каталогу, содержащему исполняемый файл
EXE_DIR = os.path.dirname(EXE_PATH)

# Путь к файлу настроек
SETTINGS_INI_PATH = os.path.join(EXE_DIR, 'settings.ini')
email = 'None'
passw = 'None'

# Создаем ConfigParser
config = configparser.ConfigParser()

onapp = False
# Если файл настроек не существует, создаем его
if not os.path.exists(SETTINGS_INI_PATH):
    with open(SETTINGS_INI_PATH, 'w') as configfile:
        configfile.write('[CONFIG]\n')
        configfile.write('email = \n')
        configfile.write('passw = \n')

# Читаем файл настроек
config.read(SETTINGS_INI_PATH)


# Гуишка
def guiapp(page: ft.Page):
    page.title = "🔥UrokJoiner v4🔥 by Feryuvva"
    page.theme_mode = 'dark'
    page.window_width = 430
    page.window_height = 270
    page.window_resizable = False
    page.vertical_alignment=ft.MainAxisAlignment.CENTER

    def changetheme(e):
        if page.theme_mode == 'dark':
            page.theme_mode = 'light'  
        else:
            page.theme_mode = 'dark' 
        page.update()

    def autojoin(e):
        global main_thread
        global onapp
        print('Button press')
        print(onapp)
        if '@' in config['CONFIG']['email'] and onapp == False:
            onapp = True
            autojoinbutton.text = 'Auto-Join On'
            page.update()
            asyncio.run(start_main())
        elif onapp == True:
            try:
                onapp = False
            except:
                pass
            autojoinbutton.text = 'Auto-Join Off'
            page.update()
            main_thread = None
        else:
            print('Else')


    def passinput(e):
            config.read(SETTINGS_INI_PATH)
            if passwtextfield.value != config["CONFIG"]['passw']:
                config["CONFIG"]['passw'] = passwtextfield.value
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)

    def submit(e):
        config.read(SETTINGS_INI_PATH)
        if emailtextfield.value != config["CONFIG"]['email'] and passwtextfield.value != config["CONFIG"]['passw']:
            config["CONFIG"]['email'] = emailtextfield.value
            config["CONFIG"]['passw'] = passwtextfield.value
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
    def emailinput(e):
            config.read(SETTINGS_INI_PATH)
            if emailtextfield.value != config["CONFIG"]['email']:
                config["CONFIG"]['email'] = emailtextfield.value
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
    def visiblepassword(e):
        if passwtextfield.password:
            passwtextfield.password = False
        else:
            passwtextfield.password = True
        page.update()
    
    data = config['CONFIG']
    if data['email'] != "None":
        emailtextfield = ft.TextField(value=data['email'],label='Enter email', on_submit=emailinput)
    else:
        emailtextfield = ft.TextField(label='Enter email', on_submit=emailinput)


    if data['passw'] != "None":
        passwtextfield = ft.TextField(value=data['passw'],label='Enter password', on_submit=passinput, password=True)
    else:
        passwtextfield = ft.TextField(label='Enter password', on_submit=passinput, password=True)


    chngthembutton = ft.IconButton(icon=ft.icons.SUNNY, on_click=changetheme)
    checkpasswordbutton = ft.IconButton(icon=ft.icons.REMOVE_RED_EYE, on_click=visiblepassword)



    autojoinbutton = ft.OutlinedButton(text='Auto-Join Off', on_click=autojoin)

    submitbutton = ft.OutlinedButton('Submit', on_click=submit)



    github = ft.IconButton(icon=ft.icons.MESSAGE, url="https://github.com/Feryuvva")
    discord = ft.IconButton(icon=ft.icons.DISCORD, url="https://discordapp.com/users/1016393252972273764/")

    mainrow = ft.Row(
        [
            ft.Column([            
                emailtextfield,
                ft.Row([
                    passwtextfield,
                    checkpasswordbutton
                ]),
                
                ft.Row([
                    submitbutton,
                    autojoinbutton
                ])
            ]),
        ], alignment=ft.MainAxisAlignment.CENTER
    )
    row_left_down = ft.Row([
        chngthembutton,
        github,
        discord
    ], alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.VerticalAlignment.END
    )
    page.add(
        mainrow,
        row_left_down
    )

# Нажимает розклад и выбирает урок
def joinonlesson(browser):
    print('start joinonlesson')
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
        if hours >= 12:
            numberoflesson -= 1
        if hours == 11:
            return
    print(numberoflesson)
    try:
        number = lessons[now.weekday()][numberoflesson]
    except KeyError:
        return
    print('start try')
    sleep(3)
    try:
        uroki = browser.find_elements(By.CLASS_NAME, "calendar-event-subject")
        urok = 1
        for i in uroki:
            if urok == number:
                jointolessonhuman = ActionChains(browser).click(i)
                jointolessonhuman.perform()
                break
            urok += 1
    except Exception as e: 
        print(e)
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
    url = f"{browser.current_url}".replace('http', ' http').split(' ')
    if len(url) > 2:
        url = url[2]
    else:
        url = url[1]
    os.system(f'start {url}')
    print(url)
    if 'meet.google' in url:
        sleep(15)
        pyautogui.hotkey('f11')
        sleep(2)
        pyautogui.hotkey('ctrl', 'd')
        sleep(2)
        pyautogui.hotkey('ctrl', 'e')
        sleep(2)
        pyautogui.moveTo(1336, 517)
        sleep(2)
        pyautogui.click()
    else:
        sleep(15)
        pyautogui.moveTo(1005, 600)
        pyautogui.click()
    return



# Вход в хюман + нажатие на 141 лицей
def login(username, parol):
    try:
        options = Options()
        options.add_argument(f'user-agent={fake_useragent.UserAgent}')
        options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")

        browser = webdriver.Chrome(options=options)
        browser.set_window_size(1920, 1080)
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
        return
# Запуск мейна лоигчно?
def start_main():
    print(f"onapp = {onapp} try start main()!")
    print(onapp)
    while onapp == True:
        print('main()')
        main()
    else:
        return
    

# Запуск функции захода на урок вприцнипе, задержки между уроками и так далее
def main():
    global onapp
    print('start main()')
    try:
        data = config['CONFIG']
        email = data['email']
        passw = data['passw']
        now = datetime.datetime.now()
        hours = now.hour
        print(hours)
        print(type(now.minute))
        if 8 <= hours <= 15 and email != 'None' and passw != 'None':
            if hours == 8 and now.minute >= 30:
                print('start 9')
                login(email, passw)
                sleep(((60 - now.minute) + 23)*60)
            if (9 == hours or 10 == hours or 11 == hours or 12 == hours) and now.minute >= 25:
                print('start 9, 10, 11, 12')
                login(email, passw)
                sleep(((60 - now.minute) + 18)*60)
            if hours == 13 and now.minute >= 20:
                print('start 13')
                login(email, passw)
                sleep(((60 - now.minute) + 13)*60)
            if 14 == hours and now.minute >= 15:
                print('start 14')
                login(email, passw)
                sleep(((60 - now.minute) + 8)*60)
            if hours == 15 and now.minute >= 10:
                print('start 15')
                login(email, passw)
                onapp = False
                return
            else:
                print('spatyli')
        else:
            print('check time')
            sleep(1)
    except Exception as ex:
        print(ex)





# Ура, Запускаем прогу!!
if __name__ == "__main__":
    try:
        main_thread = threading.Thread(target=start_main)
        ft.app(guiapp)
    except Exception as ex:
        print(ex)
    finally:
        onapp = False
        sys.exit()