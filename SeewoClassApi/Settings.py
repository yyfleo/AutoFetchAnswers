# coding = utf-8
import configparser
import os


class SCASettings():
    """ A simple ini file I/O operations interface for x-tokens """
    __cp = configparser.ConfigParser()

    def __init__(self, settingsFilePath=os.path.dirname(os.path.realpath(__file__)) + "\\tokens.ini"):
        self.__iniFilePath = settingsFilePath
        self.__cp.read(self.__iniFilePath)

    def getAccountsList(self):
        try:
            return self.__cp.options("x-tokens")
        except configparser.NoSectionError:
            return []

    def readSettings(self, name: str): return self.__cp.get("x-tokens", name)

    def writeSettings(self, name: str, value: str):
        try:
            self.__cp.set("x-tokens", name, value)
        except configparser.NoSectionError:
            self.__cp.add_section("x-tokens")
            self.__cp.set("x-tokens", name, value)
        with open(self.__iniFilePath, "w") as iniFile:
            self.__cp.write(iniFile)

    def deleteSettings(self, name: str):
        try:
            self.__cp.remove_option("x-tokens", name)
            return True
        except Exception:
            return False
