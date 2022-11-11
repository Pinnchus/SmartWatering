# read configuration file
import os
import ujson


class rootvalues:
    def __init__(self):
        self.host = os.system('hostname -I| awk "{print $1}"')
        self.port = str("80")
        self.wifi = bool(True)
        self.webserver = bool(False)
        self.wheatherKey= ""

class tabhomevalues:
    def __init__(self):
        self.mode = int(0)
        self.runningtime = int(0)
        self.delayed = int(0)
        self.zones = [False,False,False,False,False,False,False,False]
        self.onoff = bool(False)
        self.sensors = bool(False)
        self.smart = bool(False)
        self.weather = bool(False)

class tabsettings:
    def __init__(self):
        self.programset  = [[[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program0 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program1 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program2 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program3 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program4 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program5 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program6 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program7 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program8 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program9 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program10 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program11 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program12 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program13 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]],  #Program14 [hour,minute][runningtime by zone],RunningDays
                            [[0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]]  #Program15 [hour,minute][runningtime by zone],RunningDays
        self.Country = "Country"
        self.City = "City"
        self.CountryCode="--"
        self.GMT = None
        self.wifissid = None
        self.wifikey = None
        self.sensors = [["Name","IpAddresOrKey"],
                        ["Name","IpAddresOrKey"],
                        ["Name","IpAddresOrKey"],
                        ["Name","IpAddresOrKey"],
                        ["Name","IpAddresOrKey"],
                        ["Name","IpAddresOrKey"],
                        ["Name","IpAddresOrKey"],
                        ["Name","IpAddresOrKey"]]
        



class initConfig:

    def __init__(self, FileName="ConfigR.conf"):
        self.conffile = FileName
        if not self.file_or_dir_exists(self.conffile):
            print("ERROR: Not Config File")
            return False
        else:
            print("Read Config File")
        self.deviceconfig=rootvalues()
        self.homevalues=tabhomevalues()
        self.settings=tabsettings()
        self.configdata=None
        
        with open(FileName) as fp:
            self.configdata = ujson.loads(fp.read())
            #configdataWifissid = configdata["ssid"]
            #configdataWifipasswd = configdata["password"]
            self.deviceconfig.port = self.configdata["port"]
            self.deviceconfig.host = self.configdata["host"]
            self.deviceconfig.wifi = self.configdata["WiFi"]
            self.deviceconfig.webserver = self.configdata["WebServer"]
            self.deviceconfig.wheatherKey = self.configdata["wheatherKey"]
            self.homevalues.mode = self.configdata["TabHome"]["Mode"]
            self.homevalues.runningtime = self.configdata["TabHome"]["RunningTime"]
            self.homevalues.delayed = self.configdata["TabHome"]["Delayed"]
            for i in range (8):
                zonefind=str(i+1)
                self.homevalues.zones[i]=self.configdata["TabHome"]["Zones"][zonefind]
            self.homevalues.onoff = self.configdata["TabHome"]["OnOff"]
            self.homevalues.sensors = self.configdata["TabHome"]["Sensors"]
            self.homevalues.smart = self.configdata["TabHome"]["Smart"]
            self.homevalues.weather = self.configdata["TabHome"]["Weather"]
            for i in range (16):
                indexp=str(i)
                progfind="Program"+indexp
                self.settings.programset[i][0][0]=self.configdata["TabSettings"]["Programs"][progfind]["startHour"]
                self.settings.programset[i][0][1]=self.configdata["TabSettings"]["Programs"][progfind]["startMin"]
                for j in range(8):
                    zonefind=str(j)
                    self.settings.programset[i][1][j]=self.configdata["TabSettings"]["Programs"][progfind]["Zone"][zonefind]
                for j in range (7):
                    daysfind=str(j)
                    self.settings.programset[i][2][j]=self.configdata["TabSettings"]["Programs"][progfind]["RunningDays"][daysfind]


            self.settings.Country = self.configdata["TabSettings"]["ForeCast"]["Country"]
            self.settings.City = self.configdata["TabSettings"]["ForeCast"]["City"]
            self.settings.CountryCode = self.configdata["TabSettings"]["ForeCast"]["CountryCode"]
            self.settings.GMT = self.configdata["TabSettings"]["ForeCast"]["GMT"]
            self.settings.wifissid = self.configdata["TabSettings"]["WiFi"]["ssid"]
            self.settings.wifikey = self.configdata["TabSettings"]["WiFi"]["password"]
            for i in range(8):
                self.settings.sensors[i][0]=self.configdata["TabSettings"]["Sensors"][str(i)]["Name"]
                self.settings.sensors[i][1]=self.configdata["TabSettings"]["Sensors"][str(i)]["Key"]

            #print("######"self.homevalues)
            print("Host %s" % self.deviceconfig.host )
            fp.close()
            

    def file_or_dir_exists(self, filename):
        try:
            os.stat(filename)
            return True
        except OSError:
            return False


    def confWrite(self):
        with open(self.conffile, 'w+') as json_file:
            ujson.dump(self.configdata, json_file)
        json_file.close()

