#!/bin/python3

#this script will rotate your display and touch panel
#must have xinput installed
#tested on Raspbian Jessie with Pixel on 10/23/2016 on a Raspberry Pi 3
#with the Raspberry Pi Touch Display and python 3.4.2


import os

print("You are going to rotate the screen and the touch panel 90º, 180º or 270º")
str = ""
options = ["90","180","270"]
words = ["lcd_rotate=2","display_rotate=0","display_rotate=1","display_rotate=2","display_rotate=3","display_rotate=0x10000","display_rotate=0x20000"]
document = open("/boot/config.txt", "r")
doc_temp = open("/boot/doc_temp.txt", "w")

def rotate_touch(position):
    xinput_script = open("/usr/local/bin/touch-rotate.sh", "w")
    xinput_script.write("#!/bin/bash\n")
    xinput_script.write("xinput set-prop 'FT5406 memory based driver' 'Evdev Axes Swap' 1\n")
    xinput_script.write("xinput --set-prop 'FT5406 memory based driver' 'Evdev Axis Inversion' " + position + "\n")
    xinput_script.close()
    autostart = open("/home/pi/.config/lxsession/LXDE-pi/autostart", "a")
    autostart.write("@/usr/local/bin/touch-rotate.sh")
    autostart.close()
    
while str not in options: 
    str = input("Please Write 90, 180 or 270: ")

for line in document.readlines():
    splitline=line.split()
    for word in splitline:
        if word not in words:
            doc_temp.write(line)
        
if str == "90":
    doc_temp.write("\ndisplay_rotate=1")
    rotate_touch("0 1")    
elif str == "180":
    doc_temp.write("\nlcd_rotate=2")
    
elif str == "270":
    doc_temp.write("\ndisplay_rotate=3")
    rotate_touch("1 0") 

document.close()
doc_temp.close()
doc_temp = open("/boot/doc_temp.txt", "r")
document = open("/boot/config.txt", "w")
for line in doc_temp.readlines():
    document.write(line)
document.close()
doc_temp.close()
os.remove("/boot/doc_temp.txt")
