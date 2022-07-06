import os
import subprocess as sp

paths = {
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'chrome': "C:\\Program Files\\Google\\Chrome\\Application\\chrome",
    'vscode': "C:\\Users\\Mehrshad\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"

}


def execute(query):
    if 'cmd' in query:
        speak('cmd')
        open_cmd()
    if 'camera' in query:
        ops.open_camera()
    if 'calculator' in query:
        print('calculator')
        open_app('calculator')
    if 'chrome' in query:
        open_app('chrome')
    if 'code' in query:
        open_app('vscode')




def open_cmd():
    print('cmd starting')
    os.system('start cmd')

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def open_app(name):
    print(paths[name])
    os.startfile(paths[name])
