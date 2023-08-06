# !/usr/bin/env python
# -*- coding:utf-8 -*-
import PySimpleGUI as sg

sg.theme("DarkAmber")

layout = [
    [sg.Text("unput file name")],
    [sg.Text("filename"), sg.InputText()],
    [sg.Button("enter"), sg.Button("cancel")],
]

windows = sg.Window("print file name", layout)


def activate():
    while True:
        event, value = windows.read()
        if event == sg.WINDOW_CLOSED or event == "cancel":
            break
        print(f"input content:{value[0]}")
    windows.close()


if __name__ == '__main__':
    activate()
