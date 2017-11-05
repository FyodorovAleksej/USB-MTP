import subprocess
import os
import re

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox


class UsbAdapter(QObject):
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
            if (usbInfo["mountPoint"]!= "\n" and usbInfo["size"] != None):
                usbList.append(usbInfo)
        logfile.close()
        return usbList

    def getUsbInfo(self, name):
        usbInfo = {"name": None, "mountPoint": None, "size": None}
        subprocess.call("lsblk -p | grep " + name + " > " + os.getcwd() + "/log.txt", shell=True)
        logfile = open(os.getcwd() + "/log.txt", "r+")
        line = logfile.readline()
        if (line != None):
            s = re.split(r" +", line)
            dev = s[0][s[0].index("/"):]
            usbInfo["name"] = dev
            mount = s[6]
            usbInfo["mountPoint"] = mount
            subprocess.call("df -hm | grep " + name + " > " + os.getcwd() + "/memory.txt", shell=True)
            memoryfile = open(os.getcwd() + "/memory.txt")
            memdict = {"all": 0, "free": 0, "used": 0}
            line = memoryfile.readline()
            if(line != None):
                result = re.split(r" +", line)
                if (len(result) >= 3):
                    memdict["all"] = memdict["all"] + int(result[1])
                    memdict["used"] = memdict["used"] + int(result[2])
                    memdict["free"] = memdict["free"] + int(result[3])
                usbInfo["size"] = memdict
            memoryfile.close()
        logfile.close()
        return usbInfo

    def mtpDevice(self):
        subprocess.call("mtp-detect > " + os.getcwd() + "/mtp.txt", stderr = None, shell = True)
        mtpfile = open(os.getcwd() + "/mtp.txt", "r+")
        mtpList = []
        text = mtpfile.read()
        mtpfile.close()
        current = 0
        while(current != -1):
            memdict = {"all": 0, "free": 0, "used": 0}
            current = text.find("@", current)
            usbInfo = {"name": None, "mountPoint": None, "size": None}
            if (current != -1):
                current = text.find("MaxCapacity:",current)
                next = text.find("FreeSpaceInBytes:",current)
                memdict["all"] = int(text[current:next].split(":")[1])//1024//1024
                current = next
                next = text.find("FreeSpaceInObjects:",current)
                memdict["free"] = int(text[current:next].split(":")[1])//1024//1024
                memdict["used"] = memdict["all"] - memdict["free"]
                current = next
                current = text.find("StorageDescription:",current)
                next = text.find("VolumeIdentifier:",current)
                usbInfo["name"] = text[current:next].split(":")[1]
                usbInfo["size"] = memdict
            usbInfo["mountPoint"] = "-"

            if (usbInfo["mountPoint"] != "\n" and usbInfo["size"] != None):
                mtpList.append(usbInfo)
        return mtpList

    def eject(self, name):
        if (name != "-"):
            ejectFile = open(os.getcwd() + "/eject.txt", "w+")
            subprocess.call("eject " + name, stderr=ejectFile ,shell=True, timeout=3)
            ejectFile.close()
            ejectFile = open(os.getcwd() + "/eject.txt", "r+")
            message = ejectFile.read()
            ejectFile.close()
            if (message.find("target is busy") > 0):
                return "target is busy"
            elif (message.find("is not mounted") > 0):
                return "target is not mounted"
            else:
                subprocess.call("sudo eject " + name, shell=True, timeout=3)
                return None