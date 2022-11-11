try:
    import usocket as _socket
except:
    import _socket
try:
    import ussl as ssl
except:
    import ssl
import ujson
import time
import lvgl as lv

class forecast:
    def __init__(self):
        self.currentFC = {"sunrise": 1667900166, "sunset": 1667949367, "temp" : 21.86, "pressure" : 1015, "humidity" : 49, "dew_point" : 10.68, "cloudiness" : 99, "windspeed" : 4.12, "description" : "overcast clouds", "icon" : "04d", "temp_min" : 10.1, "temp_max" : 15.2}
        self.tomorrowFC = {"sunrise": 1667900166, "sunset": 1667949367, "temp" : 21.86, "pressure" : 1015, "humidity" : 49, "dew_point" : 10.68, "cloudiness" : 99, "windspeed" : 4.12, "description" : "overcast clouds", "icon" : "04d", "temp_min" : 10.1, "temp_max" : 15.2}
        self.afterTomorrowFC = {"sunrise": 1667900166, "sunset": 1667949367, "temp" : 21.86, "pressure" : 1015, "humidity" : 49, "dew_point" : 10.68, "cloudiness" : 99, "windspeed" : 4.12, "description" : "overcast clouds", "icon" : "04d", "temp_min" : 10.1, "temp_max" : 15.2}
        self.graphics = None

    def getForecast(self, openweatherkey):
        key=openweatherkey
        s = _socket.socket()
        ai = _socket.getaddrinfo("ip-api.com", 80)
        addr = ai[0][-1]
        s.connect(addr)
        s.write(b"GET /json/ HTTP/1.0\r\n\r\n")
        var=s.read(4096)
        s.close()
        var=var.decode()
        jsonstring=jsonstring=str(var[var.find('{'):len(var)])
        location=ujson.loads(jsonstring)
        status=location["status"]
        countryName= location["country"]
        countryCode=location["countryCode"]  
        countryRegion=location["region"]
        RegionName=location["regionName"]
        Querycity=location["city"]          
        lat=location["lat"]
        lon=location["lon"]
        #"http://api.openweathermap.org/data/2.5/onecall?units=metric&appid=KEY&lat=-33.6167&lon=-70.5833"
        query="/data/2.5/onecall?"
        s = _socket.socket()
        ai = _socket.getaddrinfo("api.openweathermap.org", 443)
        addr = ai[0][-1]
        s.connect(addr)
        s = ssl.wrap_socket(s)
        query="GET "+query+"&units=metric&appid="+key+"&lat="+str(lat)+"&lon="+str(lon)+" HTTP/1.0\r\n\r\n"
        s.write(query)
        var=s.read(32768)
        s.close()
        var=var.decode()
        jsonstring=str(var[var.find('{'):len(var)])
        jsonforecast=ujson.loads(jsonstring)

        time_offset = jsonforecast["timezone_offset"]
        self.currentFC["sunrise"]=jsonforecast["current"]["sunrise"]+time_offset
        self.currentFC["sunset"]=jsonforecast["current"]["sunset"]+time_offset
        self.currentFC["temp"]=jsonforecast["current"]["temp"]
        self.currentFC["pressure"]=jsonforecast["current"]["pressure"]
        self.currentFC["humidity"]=jsonforecast["current"]["humidity"]
        self.currentFC["dew_point"]=jsonforecast["current"]["dew_point"]
        self.currentFC["cloudiness"]=jsonforecast["current"]["clouds"]
        self.currentFC["windspeed"]=jsonforecast["current"]["wind_speed"]
        self.currentFC["description"]=jsonforecast["current"]["weather"][0]["description"]
        self.currentFC["icon"]=jsonforecast["current"]["weather"][0]["icon"]
        self.currentFC["temp_min"]=jsonforecast["daily"][0]["temp"]["min"]
        self.currentFC["temp_max"]=jsonforecast["daily"][0]["temp"]["max"]
        #print(currentFC)
        self.tomorrowFC["sunrise"]=jsonforecast["daily"][1]["sunrise"]+time_offset
        self.tomorrowFC["sunset"]=jsonforecast["daily"][1]["sunset"]+time_offset
        self.tomorrowFC["temp"]=jsonforecast["daily"][1]["temp"]["day"]
        self.tomorrowFC["pressure"]=jsonforecast["daily"][1]["pressure"]
        self.tomorrowFC["humidity"]=jsonforecast["daily"][1]["humidity"]
        self.tomorrowFC["dew_point"]=jsonforecast["daily"][1]["dew_point"]
        self.tomorrowFC["cloudiness"]=jsonforecast["daily"][1]["clouds"]
        self.tomorrowFC["windspeed"]=jsonforecast["daily"][1]["wind_speed"]
        self.tomorrowFC["description"]=jsonforecast["daily"][1]["weather"][0]["description"]
        self.tomorrowFC["icon"]=jsonforecast["daily"][1]["weather"][0]["icon"]
        self.tomorrowFC["temp_min"]=jsonforecast["daily"][1]["temp"]["min"]
        self.tomorrowFC["temp_max"]=jsonforecast["daily"][1]["temp"]["max"]
        #print(tomorrowFC)

        self.afterTomorrowFC["sunrise"]=jsonforecast["daily"][2]["sunrise"]+time_offset
        self.afterTomorrowFC["sunset"]=jsonforecast["daily"][2]["sunset"]+time_offset
        self.afterTomorrowFC["temp"]=jsonforecast["daily"][2]["temp"]["day"]
        self.afterTomorrowFC["pressure"]=jsonforecast["daily"][2]["pressure"]
        self.afterTomorrowFC["humidity"]=jsonforecast["daily"][2]["humidity"]
        self.afterTomorrowFC["dew_point"]=jsonforecast["daily"][2]["dew_point"]
        self.afterTomorrowFC["cloudiness"]=jsonforecast["daily"][2]["clouds"]
        self.afterTomorrowFC["windspeed"]=jsonforecast["daily"][2]["wind_speed"]
        self.afterTomorrowFC["description"]=jsonforecast["daily"][2]["weather"][0]["description"]
        self.afterTomorrowFC["icon"]=jsonforecast["daily"][2]["weather"][0]["icon"]
        self.afterTomorrowFC["temp_min"]=jsonforecast["daily"][2]["temp"]["min"]
        self.afterTomorrowFC["temp_max"]=jsonforecast["daily"][2]["temp"]["max"]

        #return self.currentFC, self.tomorrowFC, self.afterTomorrowFC

    def updateForecast(self, openweatherkey, graph=None):
        self.graphics = graph if graph else None
        self.getForecast(openweatherkey)
        stringtemp=self.currentFC["description"]
        stringtemp=stringtemp+"\nMax/Min: "+str(self.currentFC["temp_max"]) + " / " + str(self.currentFC["temp_min"]) + "C"
        stringtemp=stringtemp+"\nHum/Press: " + str(self.tomorrowFC["humidity"])+ "% / " + str(self.currentFC["pressure"]) + "hPa"
        stringtemp=stringtemp+" Wind: " + str(self.currentFC["windspeed"])
        Dyear, Dmonth, Dday, Dhour, Dmin, Dsec, Dweekday, Dyearday, unknown = time.gmtime(self.tomorrowFC["sunset"])
        sunset="{:02d}:{:02d}".format(Dhour, Dmin,)
        Dyear, Dmonth, Dday, Dhour, Dmin, Dsec, Dweekday, Dyearday, unknown = time.gmtime(self.tomorrowFC["sunrise"])
        sunrise="{:02d}:{:02d}".format(Dhour, Dmin,)
        stringtemp=stringtemp+"\nSun Rise/Set: "+ sunrise +" / "+sunset
        icon="icons/"+self.currentFC["icon"]+"@2x.png"
        try:
            with open(icon,'rb') as f:
                png_data = f.read()
        except:
            print("Could not find "+icon)
            sys.exit()

        img_icon = lv.img_dsc_t({
          'data_size': len(png_data),
          'data': png_data
        })

        self.graphics.ui_Tab2Label_HOY.set_text(stringtemp)
        self.graphics.ui_Tab2FCImg1.set_src(img_icon)

        