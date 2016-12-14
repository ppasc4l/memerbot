"""
    Ian Dansereau
    GroupMeReddit
    config.py
    5/5/16

"""
import configparser

"""
    Config object used for storing all of the configuration data from the config.ini file

"""


class Config(object):
    def __init__(self):

        self.config_file = 'config/config.ini'
        self.banned_file = 'config/blacklist.txt'
        self.moderator_file = 'config/moderators.txt'
        self.api_key = 'config/.groupy.key'

        self.config = configparser.ConfigParser()
        self.config.read(self.config_file, encoding='utf-8')

        self._groupID = self.config.get('BOT', 'groupid', fallback=None)
        self._botID = self.config.get('BOT', 'botid', fallback=None)
        self._prefix = self.config.get('BOT', 'prefix', fallback='!')

        self.admin = self.config.get('ADMIN', 'adminid', fallback=None)
        self.moderators = self.getMods()
        self.banned = self.getBanned()
        self.nsfw = self.config.getboolean('ADMIN', 'nsfw', fallback=False)

    def getConfigFile(self):
        return self.config_file

    def setNsfw(self, nsfw):
        self.config.read(self.config_file, encoding='utf-8')
        self.config.set('ADMIN', 'nsfw', nsfw)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def getBanned(self):
        banned = set()
        with open(self.banned_file, 'r+') as file:
            for userid in file.read().split():
                banned.add(userid)
            file.close()
        return banned

    def getMods(self):
        mods = set()
        with open(self.moderator_file, 'r+') as file:
            for userid in file.read().split():
                mods.add(userid)
            file.close()
        return mods

    def addBanned(self, userid):
        if userid not in self.banned:
            with open(self.banned_file, 'a') as file:
                file.write(" " + userid)
            file.close()
            self.banned = self.getBanned()

    def addMod(self, userid):
        if userid not in self.moderators:
            with open(self.moderator_file, 'a') as file:
                file.write(" " + userid)
            file.close()
            self.moderators = self.getMods()

    def removeBanned(self, userid):
        if userid in self.banned:
            self.banned.remove(userid)
            with open(self.banned_file, 'w') as file:
                for id in self.banned:
                    file.write(" " + id)

    def removeMod(self, userid):
        if userid in self.moderators:
            self.moderators.remove(userid)
            with open(self.moderator_file, 'w') as file:
                for id in self.moderators:
                    file.write(" " + id)
