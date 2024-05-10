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





text11 = ft.Checkbox('')
text12 = ft.Checkbox('')
text13 = ft.Checkbox('')
text14 = ft.Checkbox('')
text15 = ft.Checkbox('')
text16 = ft.Checkbox('')
text17 = ft.Checkbox('')
text18 = ft.Checkbox('')
text21 = ft.Checkbox('')
text22 = ft.Checkbox('')
text23 = ft.Checkbox('')
text24 = ft.Checkbox('')
text25 = ft.Checkbox('')
text26 = ft.Checkbox('')
text27 = ft.Checkbox('')
text28 = ft.Checkbox('')
text31 = ft.Checkbox('')
text32 = ft.Checkbox('')
text33 = ft.Checkbox('')
text34 = ft.Checkbox('')
text35 = ft.Checkbox('')
text36 = ft.Checkbox('')
text37 = ft.Checkbox('')
text38 = ft.Checkbox('')
text41 = ft.Checkbox('')
text42 = ft.Checkbox('')
text43 = ft.Checkbox('')
text44 = ft.Checkbox('')
text45 = ft.Checkbox('')
text46 = ft.Checkbox('')
text47 = ft.Checkbox('')
text48 = ft.Checkbox('')
text51 = ft.Checkbox('')
text52 = ft.Checkbox('')
text53 = ft.Checkbox('')
text54 = ft.Checkbox('')
text55 = ft.Checkbox('')
text56 = ft.Checkbox('')
text57 = ft.Checkbox('')
text58 = ft.Checkbox('')



checkboxesurokiMon = [text11, text12, text13, text14, text15, text16, text17, text18]
checkboxesurokiTue = [text21, text22, text23, text24, text25, text26, text27, text28]
checkboxesurokiWed = [text31, text32, text33, text34, text35, text36, text37, text38]
checkboxesurokiThu = [text41, text42, text43, text44, text45, text46, text47, text48]
checkboxesurokiFri = [text51, text52, text53, text54, text55, text56, text57, text58]

checkboxesuroki = [text11, text12, text13, text14, text15, text16, text17, text18,
text21, text22, text23, text24, text25, text26, text27, text28,
text31, text32, text33, text34, text35, text36, text37, text38,
text41, text42, text43, text44, text45, text46, text47, text48,
text51, text52, text53, text54, text55, text56, text57, text58
]


# Создаем ConfigParser
config = configparser.ConfigParser()

onapp = False
# Если файл настроек не существует, создаем его
if not os.path.exists(SETTINGS_INI_PATH):
    with open(SETTINGS_INI_PATH, 'w') as configfile:
        configfile.write('[CONFIG]\n')
        configfile.write('email = None\n')
        configfile.write('passw = None\n')
        configfile.write('lessons = None\n')

# Читаем файл настроек
config.read(SETTINGS_INI_PATH)


# Гуишка
def guiapp(page: ft.Page):
    page.title = "🔥UrokJoiner v4🔥 by Feryuvva"
    page.window_top = 250
    page.window_left = 550
    page.theme_mode = 'dark'
    page.window_width = 430         #430
    page.window_height = 330        #270
    page.window_resizable = False
    page.vertical_alignment=ft.MainAxisAlignment.CENTER


    def changepages(e):
        pages = [mainpage, settingspage]
        page.clean()
        if page.navigation_bar.selected_index == 1:
            page.add(pages[1])
            page.window_width = 650
            page.window_height = 500
            page.window_top = 170
            page.window_left = 450
        else:
            page.add(pages[0])
            page.window_width = 430
            page.window_height = 330
            page.window_top = 250
            page.window_left = 550
        page.update()


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
            print(config['CONFIG']['lessons'])
            config["CONFIG"]['email'] = emailtextfield.value
            config["CONFIG"]['passw'] = passwtextfield.value
            with open('settings.ini', 'w') as configfile:
                i = 0
                lessons = {
                    0: [],
                    1: [],
                    2: [],
                    3: [],
                    4: [],
                }
                print(str(lessons))
                for text in checkboxesurokiMon:
                    if text.value:
                        i += 1
                        lessons[0].append(i)
                for text in checkboxesurokiTue:
                    if text.value:
                        i += 1
                        lessons[1].append(i)
                for text in checkboxesurokiWed:
                    if text.value:
                        i += 1
                        lessons[2].append(i)
                for text in checkboxesurokiThu:
                    if text.value:
                        i += 1
                        lessons[3].append(i)
                for text in checkboxesurokiFri:
                    if text.value:
                        i += 1
                        lessons[4].append(i)
                config["CONFIG"]['lessons'] = str(lessons)
                config.write(configfile)
            print(str(lessons))


        
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
    def openhuman(e):
        os.system(f"start https://lms.human.ua/app/calendar")
    
    data = config['CONFIG']
    lessons = eval(data['lessons'])
    print(range(len(lessons[2])))
    if data['lessons'] != 'None':
        for i in range(len(lessons[0])):checkboxesurokiMon[i].value = True
        for i in range(len(lessons[1])):checkboxesurokiTue[i].value = True
        for i in range(len(lessons[2])):checkboxesurokiWed[i].value = True
        for i in range(len(lessons[3])):checkboxesurokiThu[i].value = True
        for i in range(len(lessons[4])):checkboxesurokiFri[i].value = True

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
    openHumanbutton = ft.OutlinedButton('Open HUMAN', on_click=openhuman)


    github = ft.IconButton(icon=ft.icons.MESSAGE, url="https://github.com/Feryuvva")
    discord = ft.IconButton(icon=ft.icons.DISCORD, url="https://discordapp.com/users/1016393252972273764/")

    mainpage = ft.Row(
        [
            ft.Column([
                autojoinbutton,
                openHumanbutton,
                ft.Row([
                    chngthembutton,
                    github,
                    discord
                ])
            ], alignment=ft.MainAxisAlignment.CENTER),

        ])
    settingspage = ft.Row(
        [
            ft.Column([            
                emailtextfield,
                ft.Row([
                    passwtextfield,
                    checkpasswordbutton
                ]),
                ft.Row([
                    chngthembutton,
                    github,
                    discord,
                    ft.Text('                 '),
                    submitbutton,
                ])
            ]),
            ft.Column([
                
                ft.Row([
                    ft.Text('   '),
                    ft.Text('Mon '),
                    ft.Text('Tue '),
                    ft.Text('Wed '),
                    ft.Text('Thu   '),
                    ft.Text('Fri '),
                ]),
                ft.Row([
                    ft.Text('1'),
                    text11,
                    text21,
                    text31,
                    text41,
                    text51
                    ]),
                ft.Row([
                    ft.Text('2'),
                    text12,
                    text22,
                    text32,
                    text42,
                    text52
                    ]),
                ft.Row([
                    ft.Text('3'),
                    text13,
                    text23,
                    text33,
                    text43,
                    text53
                    ]),
                ft.Row([
                    ft.Text('4'),
                    text14,
                    text24,
                    text34,
                    text44,
                    text54
                    ]),
                ft.Row([
                    ft.Text('5'),
                    text15,
                    text25,
                    text35,
                    text45,
                    text55
                    ]),
                ft.Row([
                    ft.Text('6'),
                    text16,
                    text26,
                    text36,
                    text46,
                    text56
                    ]),
                ft.Row([
                    ft.Text('7'),
                    text17,
                    text27,
                    text37,
                    text47,
                    text57
                    ]),
                ft.Row([
                    ft.Text('8'),
                    text18,
                    text28,
                    text38,
                    text48,
                    text58
                    ])
            ]),
            
        ],
    )



    page.navigation_bar = ft.NavigationBar(destinations=[
        ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
        ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings")
    ],
    on_change=changepages,
    height=65
    )


    page.add(
        mainpage
    )

# Нажимает розклад и выбирает урок
def joinonlesson(browser):
    print('start joinonlesson')
    now = datetime.datetime.now()
    hours = now.hour
    lessons = config['CONFIG']['lessons']
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