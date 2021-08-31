# Description
Simple GUI based mouse clicks automation using image detection built from non-GUI version: https://github.com/well-c/image_autoclicks

# Requirements
1) Install python
2) Install python libraries:
   pip install pyautogui keyboard numpy opencv-python

# How it works
1. Dump all your captured images in "input_images" folder
2. Start the script by double clicking "Autoclick.py" or run in CLI: python Autoclick.py
3. Default images are examples from windows 10 icon. 
4. On first "Main" tab, File = Your file name, LC = Left Click, RC = Right Click 
5. On second "Settings" tab, configure your desired settings.
6. Click "Start Automation". If you are using default configurations, you should be able to see the mouse movement between windows 10 and folder.
7. Press "Escape" anytime to quit
