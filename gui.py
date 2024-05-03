import flet as ft
import keyboard
import json
import multiprocessing
import sys
import os

import configparser

# Получаем путь к включенным файлам
PATH = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
config = configparser.ConfigParser()
config.read("settings.ini")
sldksg = None


os.path.join(PATH, 'settings.ini')
os.path.join(PATH, 'app.py')

def waitbindkey():
    global sldksg
    while True:
        print('button')
        with open(f'{PATH}\\settings.json', 'r') as bindkeycheck:
            data = json.load(bindkeycheck)
            print(data)
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == data['bind_key']:
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
            with open(f'{PATH}\\settings.json', 'r') as dgjadf:
                datadgjadf = json.load(dgjadf)
                with open(f'{PATH}\\settings.json', 'w') as bindk:
                    datadgjadf['bind_key'] = event.name
                    json.dump(datadgjadf, bindk)
            text = datadgjadf['bind_key'].upper()
            autojoinbind.text = f"Кнопка {text}"
            autojoinonbindkey = False
        page.update()

    def passinput(e):
        with open(f'{PATH}\\settings.json', 'r') as f:
            data = json.load(f)
            if passwtextfield.value not in data['passw']:
                with open(f'{PATH}\\settings.json', 'w') as file:
                    data['passw'] = passwtextfield.value
                    json.dump(data, file)

    def emailinput(e):
        with open(f'{PATH}\\settings.json', 'r') as f:
            data = json.load(f)
            if emailtextfield.value not in data['email']:
                with open(f'{PATH}\\settings.json', 'w') as file:
                    data['email'] = emailtextfield.value
                    json.dump(data, file)

    with open(f"{PATH}\\settings.json", 'r') as file:
        data = json.load(file)
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
    with open(f'{PATH}\\settings.json', 'r') as bindkeyjson:
        data = json.load(bindkeyjson)
        print(data['bind_key'])
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
