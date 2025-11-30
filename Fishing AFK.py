from PIL import Image, ImageGrab
import pytesseract
import pyautogui
import time
import ctypes
from ctypes.wintypes import HWND, DWORD, RECT

pytesseract_path = input(r"What is the path of your Tesseract.exe? Please put the full path (use the copy as path option via rightclicking the .exe) here. It'll look like C:\Program Files\Tesseract-OCR\tesseract.exe for instance: ")

# YOU NEED TO PUT THE FILEPATH (exactly) IN THESE QUOTATION MARKS BELOW
pytesseract_path = pytesseract_path[1:-1:1]
print(pytesseract_path)
pytesseract.pytesseract.tesseract_cmd = pytesseract_path

class Screenshot_Reader:
    def __init__(self):
        self.currentscreenshot = ""
        self.screenshotpath = r"Fishing_Afk_Screenshots\snapshot.png"
        self.total_fishes_and_runs_path = "Fishing_Afk_Screenshots/totals_data.txt"
        self.data = ''
        self.windowname = input("Window Name: ")
        self.interval = .1
        self.last_catch_iteration = 0
        self.last_catch_difference_of_iterations = 0
        self.numberoffishes = 0
        self.numberoffishuntilreset = 200
        self.numberofiterations = self.numberoffishuntilreset - 10
        self.start_time = time.time()

        
        self.total_fish_caught_alltime = 0
        self.total_times_cycled_alltime = 0
        self.total_seconds_spent_fishing = 0
        
        try:
            with open(self.total_fishes_and_runs_path, "r") as fobject:
                    data = fobject.readlines()
                    int_data = []
                    for line in data:
                        int_str = ""
                        for char in line:
                            if char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                                int_str += char
                                    
                        int_of_int_str = int(int_str)
                        int_data.append(int_of_int_str)
                        
                    self.total_fish_caught_alltime = int_data[0]
                    self.total_times_cycled_alltime = int_data[1]
                    self.total_seconds_spent_fishing = int_data[2]
                    
                    fobject.close()
                    
        except FileNotFoundError:
            with open(self.total_fishes_and_runs_path, "w") as fobject:
                concatenated_string = "Number of Fishes Caught (ALL TIME): " + str(self.total_fish_caught_alltime) + \
                                    "\nNumber of program cycles (ALL TIME): " + str(self.total_times_cycled_alltime) + \
                                    "\nSeconds Spent Fishin': " + "0"
                fobject.write(concatenated_string)
                
                fobject.close()

    def take_screenshot(self):
        window = GetWindowRectFromName(self.windowname)
        width = abs(window[0] - window[2])
        height = abs(window[1] - window[3])

        self.currentscreenshot = ImageGrab.grab(bbox=(window[0] + (int(width / 5) * 3), window[1], window[2], window[3]))
        self.currentscreenshot.save(self.screenshotpath)
        self.numberofiterations += 1

    def read_screenshot(self):
        self.data = pytesseract.image_to_string(Image.open(self.screenshotpath)).lower()

        test = 0

        for item in ["fishing bobber splashes", "ishing bobber splashes", "bobber splashes", "obber splash"]:
            if item in self.data and test != 1:
                self.last_catch_iteration = self.numberofiterations
                self.numberoffishes += 1
                self.total_fish_caught_alltime += 1
                test = 1

                pyautogui.rightClick()
                time.sleep(1)
                pyautogui.rightClick()
                time.sleep(2)

        if self.last_catch_difference_of_iterations > self.numberoffishuntilreset:
            test = False
            while test is False:
                pyautogui.rightClick()
                self.take_screenshot()
                self.data = pytesseract.image_to_string(Image.open(self.screenshotpath)).lower()

                for item in ["bobber thrown", "obber thrown", "thrown"]:
                    if item in self.data:
                        test = True
                        self.last_catch_iteration = self.numberofiterations

                    else:
                        pass

                time.sleep(3)

        self.last_catch_difference_of_iterations = self.numberofiterations - self.last_catch_iteration

    def run(self):
        while True:
            screenshot_reader_instance.take_screenshot()
            screenshot_reader_instance.read_screenshot()
            print("number of fishes: " + str(self.numberoffishes))
            print("number of times cycled: " + str(self.numberofiterations))
            print("number of cycles since last cast: " + str(self.last_catch_difference_of_iterations))
            test = 3
            while test > 0:
                test -= 1
                print("\n")
            
            self.total_times_cycled_alltime += 1
            temp_var = self.total_seconds_spent_fishing + (time.time() - self.start_time)
            
            with open(self.total_fishes_and_runs_path, "w") as fobject:
                concatenated_string = "Number of Fishes Caught (ALL TIME): " + str(self.total_fish_caught_alltime) + \
                                    "\nNumber of program cycles (ALL TIME): " + str(self.total_times_cycled_alltime) + \
                                    "\nSeconds Spent Fishin': " + str(int(temp_var))
                fobject.write(concatenated_string)
                
                fobject.close()
                
            
            

def GetWindowRectFromName(name:str):
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    # print(hwnd)
    # print(rect)
    return (rect.left, rect.top, rect.right, rect.bottom)

screenshot_reader_instance = Screenshot_Reader()

if screenshot_reader_instance.windowname == '':
    # PUT THE MOST COMMON WINDOW NAME YOU USE THIS PROGRAM WITH HERE
    screenshot_reader_instance.windowname = "Minecraft 1.21.10 Release Candidate 1 - Singleplayer"

screenshot_reader_instance.take_screenshot()
screenshot_reader_instance.read_screenshot()
screenshot_reader_instance.run()
