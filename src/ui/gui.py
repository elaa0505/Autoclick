from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import PySimpleGUI as sg
from src.data.data import images_detection

from os import path
import glob

from . import config

sg.theme('LightGrey5')

def main_layout():
    col = []
    i=2 # From action_file

    col.append([sg.T(i, size=(2, 1)), sg.InputText(default_text='No file selected', size=(30, 1), key='-FP-', enable_events=True ), sg.Checkbox('LF', default=True, key='-LF-', enable_events=True), sg.Checkbox('RC', default=False, key='-RF-', enable_events=True)])
    
    while(i < 11):
        col.append([sg.T(i, size=(2, 1)), sg.InputText(default_text='No file selected', size=(30, 1), key='-FP'+str(i)+'-', enable_events=True), sg.Checkbox('LF', default=True, key='-LF'+str(i)+'-', enable_events=True), sg.Checkbox('RC', default=False, key='-RF'+str(i)+'-', enable_events=True)])
        config.ACTION_SETTINGS_KEYS['file_path'+str(i)] = '-FP'+str(i)+'-' #appending new dictionary to json
        config.ACTION_SETTINGS_KEYS['left_click'+str(i)] = '-LF'+str(i)+'-'
        config.ACTION_SETTINGS_KEYS['right_click'+str(i)] = '-RF'+str(i)+'-'
        i=i+1
        
    col2 = sg.Column([[sg.Frame('Files:', [[sg.Column(col, size=(500,300), scrollable=True, vertical_scroll_only=True, pad=(0, 0))]])]], pad=(0, 0))

    layout = [
        [sg.T('', size=(70, 1)), ],           
        [col2],
        [sg.Button('Save Actions'), sg.Button('Save All'), sg.Cancel('Start Automation')]
    ]
    return layout

def create_settings_tab():

    layout = [
        [sg.Text('Press \'Escape\' to quit this application anytime', size=(50, 1), justification='center', font=("Helvetica", 12), relief=sg.RELIEF_RIDGE)],
        [],
        [sg.Frame('Action Interval',[
         [sg.Text('Time in seconds'), sg.InputText(default_text='1', size=(5, 1), key='-AI-', enable_events=True)]]), 
         sg.Frame('Task Interval',[
         [sg.Text('Time in seconds'), sg.InputText(default_text='1', size=(5, 1), key='-TI-', enable_events=True)]]),
         sg.Frame('Max Loop',[
         [sg.Text('Tasks Loop'), sg.InputText(default_text='2', size=(5, 1), key='-ML-', enable_events=True)]]),
         ],

        [sg.Frame('Randomize Click Position (%)',[
         [sg.Slider(range=(0, 100), orientation='h', size=(30, 10), default_value=0, tick_interval=10, key='-RP-', enable_events=True)]
         ]), sg.Frame('Randomize Time Interval (%)',[
         [sg.Slider(range=(0, 100), orientation='h', size=(30, 10), default_value=0, tick_interval=10, key='-RT-', enable_events=True)]
         ])],
        [sg.Frame('Image Recognition Accuracy (%)',[
         [sg.Slider(range=(20, 100), orientation='h', size=(30, 10), default_value=80, tick_interval=10, key='-IMAGE_THRESHOLD-', enable_events=True)]
         ])],
         
         
        [sg.Button('Save Settings', tooltip='Save Setting')]]

    return layout

def create_main_window(settings, general_settings):
    main = main_layout()
    setting = create_settings_tab()
    
    
    layout = [[sg.TabGroup(
        [[sg.Tab('Main', main), sg.Tab('Settings', setting)]],
        key='tab_group')],
    ]
    
    window = sg.Window('Autoclick', layout=layout, size=(600, 500), margins=(2, 2),
                       return_keyboard_events=True, finalize=True)    
    
    for key in config.ACTION_SETTINGS_KEYS:   # update window with the values read from settings file
        try:
            window[config.ACTION_SETTINGS_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')  
          
    for gen_key in config.GENERAL_SETTINGS_KEYS:   # update window with the values read from settings file
        try:
            window[config.GENERAL_SETTINGS_KEYS[gen_key]].update(value=general_settings[gen_key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from general_settings. Key = {gen_key}')  
            
    return window

                
def main_ui():
    window, actions_settings = None, config.load_actions(config.ACTIONS_FILE, config.DEFAULT_ACTIONS_SETTINGS )
    window, general_settings = None, config.load_general_settings(config.GENERAL_SETTINGS_FILE, config.DEFAULT_GENERAL_SETTINGS )
    window = create_main_window(actions_settings, general_settings)    
    while True:
        event, values = window.Read(timeout=100) 
        if event == "Start Automation":
            break       
        elif event == 'Save Actions':
            config.save_actions(config.ACTIONS_FILE, actions_settings, values)
            sg.popup('Settings saved')  
        elif event == 'Save Settings':
            config.save_general_settings(config.GENERAL_SETTINGS_FILE, general_settings, values)
            sg.popup('Settings saved')      
        elif event == 'Save All': 
            config.save_actions(config.ACTIONS_FILE, actions_settings, values)
            config.save_general_settings(config.GENERAL_SETTINGS_FILE, general_settings, values)
            sg.popup('Settings saved')  
        elif event in (None, 'Cancel'):   # if user closes window or clicks cancel
            os._exit(0)
            break      
   
    window.close()

