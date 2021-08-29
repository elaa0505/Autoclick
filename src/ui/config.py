
from os import path
from json import (load as jsonload, dump as jsondump)

# MAIN ACTIONS TAB-------------------------------------------------------------------------------------
ACTIONS_FILE = path.join(path.dirname(__file__), r'actions_file.cfg')
DEFAULT_ACTIONS_SETTINGS = {'file_path': 'null', 'left_click': True , 'right_click': False}
ACTION_SETTINGS_KEYS = {'file_path': '-FP-', 'left_click': '-LF-' , 'right_click': '-RF-'}
# GENERAL SETTINGS TAB-------------------------------------------------------------------------------------
GENERAL_SETTINGS_FILE = path.join(path.dirname(__file__), r'general_settings_file.cfg')
DEFAULT_GENERAL_SETTINGS = {'action_interval': 1, 'task_interval': 1, 'max_loop': 1 , 'rand_time': 0, 'rand_pos': 0, 'image_threshold': 80}
GENERAL_SETTINGS_KEYS = {'action_interval': '-AI-', 'task_interval': '-TI-', 'max_loop': '-ML-' , 'rand_time': '-RT-', 'rand_pos': '-RP-', 'image_threshold': '-IMAGE_THRESHOLD-'}

########################################## Load/Save Settings File ##########################################
def load_actions(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_actions(settings_file, settings, None)
    return settings


def save_actions(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in ACTION_SETTINGS_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[ACTION_SETTINGS_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)
    #sg.popup('Settings saved')
    
def load_general_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_general_settings(settings_file, settings, None)
    return settings


def save_general_settings(settings_file, settings, values):
    if values:      # if there are stuff specified by another window, fill in those values
        for key in GENERAL_SETTINGS_KEYS:  # update window with the values read from settings file
            try:
                settings[key] = values[GENERAL_SETTINGS_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)