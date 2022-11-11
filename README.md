# SmartWatering

###This is a work in progess
SmartWatering works in Raspberry Pi Zero W, with micropython and LVGL.
Its using 3.5RPI Display with direct FB and touch

##Current the following is running ok:

###Schedulles & Zones
 - 16 Programs with individual start times
 - 8 individual Zones by program, each with individual watering period

###Forecast 
- Forecast using openwathermap OneCall API and IP Location autodiscovering using ip-api.com

###Manual Start
- 4 Manual programming watering (All modes, can be with start delayed, so you don't need to run after pressing start)
--Selected Zones & Time
--Preselected program
--Preselected program to OFF (keep off after run)
--Selected Zones & Time to OFF (Keep off after run)

##Pending
--Sensor management
--Smart watering using weather forecast data, sensor data
--Show Sensor data graphics

#IMPORTANT

In order to get touch working, I've replaced the evedev.py (./lib/lv_bindings/driver/linux/evdev.py) with the included one. But it may not be necessary if the classes are extended correctly.


![Main](https://github.com/Pinnchus/SmartWatering/raw/main/images/Main.png)
![Forecast](https://github.com/Pinnchus/SmartWatering/raw/main/images/Forecast.png)
![Config](https://github.com/Pinnchus/SmartWatering/raw/main/images/Config.png)



###End
