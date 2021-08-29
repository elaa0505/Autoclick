import pyautogui
import cv2
import numpy

import glob
import time

import keyboard
import os
import random

from time import sleep

from threading import Thread
from src.ui import gui as ui

from src.ui import config

# Custom Variables
max_loop = 0
click_interval = 1
loop_interval = 1
threshold = 0.5 #accuracy
rand_time = 0.5 #randomize time by percent
rand_pos = 0 #randomize mouse position by percent

adjust_x = 10
adjust_y = 0

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
match_method =  cv2.TM_CCOEFF_NORMED   
            
            
def randomize(t, percent):
    return random.uniform(t*(1-percent),t*(1+percent))

def calc_pos(base, adjust, img_dim, rand_percent):
    return base+adjust+randomize(img_dim, rand_pos)
            
# search and click image in the center
def clickImage(image, thres=0.5, left_c=True):

    # grab windows print screen
    screen_img = pyautogui.screenshot() 

    screen_img_rgb = numpy.array(screen_img)
    
    # convert screen img to grayscale
    screen_img_gray = cv2.cvtColor(screen_img_rgb, cv2.COLOR_BGR2GRAY) 
    
    # read image
    template = cv2.imread(image,cv2.IMREAD_GRAYSCALE)
    template.shape[::-1]

    # search for matching image in screen
    res = cv2.matchTemplate(screen_img_gray, template, match_method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)    
    
    print("min_val: ", max_val) 
    print("max_val: ", max_val)
    
    # no image is found 
    if max_val < thres:
        return -1;    
        
    if( match_method  == cv2.TM_SQDIFF or match_method == cv2.TM_SQDIFF_NORMED ):
        matchLoc = min_loc
    else:
        matchLoc = max_loc

    pos_x = calc_pos(matchLoc[0], adjust_x, template.shape[1]/2, rand_pos)
    pos_y = calc_pos(matchLoc[1], adjust_y, template.shape[0]/2, rand_pos)
    
    # move mouse to center of image    
    pyautogui.moveTo(pos_x, pos_y, 0.5, pyautogui.easeOutQuad)    
    
    if left_c == True:
        # left click   
        pyautogui.click()     
    else:
        pyautogui.click(button='right')
        
    return 0;    


def autowrite():
    sleep(randomize(click_interval,rand_time))
    pyautogui.press('space')
    sleep(randomize(click_interval,rand_time))
    pyautogui.write('Hello world!')  
    return 0; 

#main thread
def main():
    loop = 0    
    sleep(1) 
    actions = config.load_actions(config.ACTIONS_FILE, config.DEFAULT_ACTIONS_SETTINGS )
    
    while loop < max_loop:
        # search images in input_images folder
        file = "No file Selected"
        for act in config.ACTION_SETTINGS_KEYS:   # update window with the values read from settings file
            print("act:", act)
            if 'file_path' in act:
                file = actions[act]
                print("file:", file)
                        
            if file != 'null' and file != 'No file Selected':   
                if 'left_click' in act:        
                    if actions[act] == True:
                        print("left_click file:", file)
                        clickImage(file, threshold, True)
                        sleep(randomize(click_interval,rand_time))
                elif 'right_click' in act:     
                    if actions[act] == True:
                        print("right_click file:", file)
                        clickImage(file, threshold, False)    
                        sleep(randomize(click_interval,rand_time))
        loop += 1
        
    os._exit(0)    

#interrupt thread
def key_listener():
    if keyboard.read_key() == "esc":
        print("Interrupted")
        os._exit(0)


def init_output():
    width,height=pyautogui.size()

    print("Screen ", width, "x", height)
    import getpass
    userID = getpass.getuser()
    print("userID: " + userID)
    import socket
    machineID = socket.gethostname()
    print("machineID: " + userID)

########################## main #################################        
init_output()

print("Press 'Escape' to quit this application anytime")

ui.main_ui()
print("Load general_settings")
general_settings = config.load_general_settings(config.GENERAL_SETTINGS_FILE, config.DEFAULT_GENERAL_SETTINGS )

for gen_key in config.GENERAL_SETTINGS_KEYS:   # update window with the values read from settings file
    print("general_settings[",gen_key, "]=", general_settings[gen_key] )
    if gen_key == 'action_interval':
        click_interval = int(general_settings[gen_key])
    elif gen_key == 'task_interval':   
        loop_interval = int(general_settings[gen_key])
    elif gen_key == 'max_loop':   
        max_loop = int(general_settings[gen_key])
    elif gen_key == 'rand_time':   
        rand_time = float(general_settings[gen_key])/100
    elif gen_key == 'rand_pos':   
        rand_pos = int(general_settings[gen_key])/100        
    elif gen_key == 'image_threshold':   
        threshold = float(general_settings[gen_key])/100        

print("click_interval=", click_interval )
print("loop_interval=", loop_interval )
print("max_loop=", max_loop )
print("rand_time=", rand_time )
print("rand_pos=", rand_pos )
print("threshold=", threshold )

thread1 = Thread(target = main)
thread2 = Thread(target = key_listener)

thread1.start()
thread2.start()

thread1.join()
thread2.join()


 
