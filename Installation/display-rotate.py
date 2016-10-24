#!/bin/python3

#this script will rotate your display and touch panel
#must have xinput installed
#tested on Raspbian Jessie with Pixel on 10/23/2016 on a Raspberry Pi 3
#with the Raspberry Pi Touch Display and python 3.4.2


import os

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)

def rotate_touch(position):
    xinput_script = open("/usr/local/bin/touch-rotate.sh", "w")
    xinput_script.write("#!/bin/bash\n")
    xinput_script.write("xinput set-prop 'FT5406 memory based driver' 'Evdev Axes Swap' 1\n")
    xinput_script.write("xinput --set-prop 'FT5406 memory based driver' 'Evdev Axis Inversion' " + position + "\n")
    xinput_script.close()
    delete_words(["@/usr/local/bin/touch-rotate.sh"],"/home/pi/.config/lxsession/LXDE-pi/autostart" )
    autostart = open("/home/pi/.config/lxsession/LXDE-pi/autostart", "a")
    autostart.write("@/usr/local/bin/touch-rotate.sh")
    autostart.close()
    make_executable("/usr/local/bin/touch-rotate.sh")

def delete_words(words, path):#words is a list of possible strings you want to substract
    document = open(path, "r")
    lines = document.readlines()
    document.close()
    document = open(path, "w")
    for line in lines:
        if line[0] != "#":
            line_copy=line
            splitline = line.split()
            for word in splitline:
                if word not in words:
                    flag=True
                else:
                    flag=False
                    break
            if flag:
                document.write(line_copy)
                flag=False
            
    document.close()

print("You are going to rotate the screen and the touch panel 90º, 180º or 270º")

str = ""
words = ["lcd_rotate=2","display_rotate=0","display_rotate=1","display_rotate=2","display_rotate=3","display_rotate=0x10000","display_rotate=0x20000"]

while str not in ["90","180","270"]: 
    str = input("Please Write 90, 180 or 270: ")

delete_words(words,"/boot/config.txt")
document = open("/boot/config.txt", "a")

if str == "90":
    document.write("\ndisplay_rotate=1")
    rotate_touch("0 1")
    
elif str == "180":
    document.write("\nlcd_rotate=2")
    delete_words(["@/usr/local/bin/touch-rotate.sh"],"/home/pi/.config/lxsession/LXDE-pi/autostart" )
    
elif str == "270":
    document.write("\ndisplay_rotate=3")
    rotate_touch("1 0")

document.close()

