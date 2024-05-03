import flet as ft
import keyboard
import json
import multiprocessing
import sys
import os

import configparser

# Получаем путь к включенным файлам
PATH = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
os.path.join(PATH, 'app.py')
config = configparser.ConfigParser()
config.read("settings.ini")
sldksg = None

import app

def waitbindkey():
    global sldksg
    while True:
            config.read("settings.ini")
            event = keyboard.read_event()
            print(event.name)
            print('\n')
            print(config["CONFIG"]['bind_key'])
            if event.event_type == keyboard.KEY_DOWN and event.name == config["CONFIG"]['bind_key']:
                if sldksg is None or not sldksg.is_alive():
                    sldksg = multiprocessing.Process(target=app.main)
                    sldksg.start()
                    print('start thread')
                elif sldksg.is_alive():
                    try:
                        sldksg.terminate()
                        sldksg.join()
                    except Exception as ex:
                        print(ex)

def guiapp(page: ft.Page):
    page.title = "🔥UrokJoiner🔥"
    page.theme_mode = 'dark'
    page.window_width = 550
    page.window_height = 450
    page.vertical_alignment=ft.MainAxisAlignment.CENTER

    def changetheme(e):
        if page.theme_mode == 'dark':
            page.theme_mode = 'light'  
        else:
            page.theme_mode = 'dark' 
        page.update()

    def autojoin(e):
        global sldksg
        if sldksg is None or not sldksg.is_alive():
            sldksg = multiprocessing.Process(target=app.main)
            sldksg.start()
            print('start thread')
            autojoinbutton.text = 'Auto-Join On'
            page.update()
        elif sldksg.is_alive():
            try:
                sldksg.terminate()
                sldksg.join()
            except:
                return
            autojoinbutton.text = 'Auto-Join Off'
            page.update()

    def bindkey(e):  
        global autojoinonbindkey
        autojoinonbindkey = True
        autojoinbind.text = "Wait..."  
        page.update()
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            config["CONFIG"]['bind_key'] = event.name
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            text = config["CONFIG"]['bind_key']
            autojoinbind.text = f"Кнопка {text}"
            autojoinonbindkey = False
        page.update()

    def passinput(e):
        if passwtextfield.value != config["CONFIG"]['passw']:
            config["CONFIG"]['passw'] = passwtextfield.value
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)

    def emailinput(e):
        if emailtextfield.value != config["CONFIG"]['email']:
            config["CONFIG"]['email'] = emailtextfield.value
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)

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

    autojoinbutton = ft.OutlinedButton('Auto-Join Off', on_click=autojoin)
    data = config['CONFIG']
    text = data['bind_key'].upper()
    autojoinbind = ft.TextButton(f"Кнопка {text}", on_click=bindkey)

    mainrow = ft.Row(
        [
            ft.Column([            
                autojoinbutton,
                autojoinbind,
                emailtextfield,
                passwtextfield
            ]),
        ], alignment=ft.MainAxisAlignment.CENTER
    )
    row_left_down = ft.Row([
        chngthembutton
    ], alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.VerticalAlignment.END
    )
    config_path = os.path.join(PATH, 'settings.json')
    page.add(
        mainrow,
        row_left_down
    )

def ftappgui():
    ft.app(guiapp)

if __name__ == "__main__":
    proces = multiprocessing.Process(target=waitbindkey)
    try:
        proces.start()
        ftappgui()
    finally:
        proces.terminate()
        sys.exit()
