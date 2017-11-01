import subprocess
import os
import re

from PyQt5.QtWidgets import QMessageBox


class UsbAdapter:
    def getUsbList(self):
        subprocess.call("lsblk -p | grep 'sd[^a][0-9]' > " + os.getcwd() + "/log.txt", shell=True)
        logfile = open(os.getcwd() + "/log.txt", "r+")
        usbList = []
        for i in logfile:
            s = re.split(r" +", i)
            usbInfo = {"name": None, "mountPoint": None, "size": None}
            dev = s[0][s[0].index("/"):]
            usbInfo["name"] = dev

            mount = s[6]
            usbInfo["mountPoint"] = mount
            subprocess.call("df -hm | grep " + dev + " > " + os.getcwd() + "/memory.txt", shell=True)
            memoryfile = open(os.getcwd() + "/memory.txt")

            # saving memory
            memdict = {"all": 0, "free": 0, "used": 0}
            line = memoryfile.readline()
            result = re.split(r" +", line)
            if (len(result) >= 3):
                memdict["all"] = memdict["all"] + int(result[1])
                memdict["used"] = memdict["used"] + int(result[2])
                memdict["free"] = memdict["free"] + int(result[3])
            usbInfo["size"] = memdict
            memoryfile.close()
            usbList.append(usbInfo)
        logfile.close()
        return usbList

    def eject(self, name):
        subprocess.call("sudo eject " + name + " > " + os.getcwd() + "/eject.txt",shell=True)
        ejectFile = open(os.getcwd() + "/eject.txt", "r+")
        message = ejectFile.read()
        if (message != None):
            error = QMessageBox(self)
            error.setText(message)

