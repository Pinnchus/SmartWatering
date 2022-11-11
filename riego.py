import lvgl as lv
import fb
import evdev
import time
import interface
import configread
import eventmngr 
import forecast


horaactual=None
scr=None






#Main 
def realmain(timerClock):
    if graphics.ui_SwitchOnOff.has_state(lv.STATE.CHECKED):
        #print("Esta en On")  #DEBUG
        emngr.CheckPrograms()





conf=configread.initConfig()
fc=forecast.forecast()
#currentFC, tomorrowFC, aftertmrwFC = fc.getForecast(conf.deviceconfig.wheatherKey)
#print(currentFC, tomorrowFC, aftertmrwFC)
lv.init()
fb.init()

# Register FB display driver

disp_buf1 = lv.disp_draw_buf_t()
buf1_1 = bytes(480*10)
disp_buf1.init(buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
disp_drv.init()
disp_drv.draw_buf = disp_buf1
disp_drv.flush_cb = fb.flush
disp_drv.hor_res = 480
disp_drv.ver_res = 320
disp_drv.register()

scr = lv.scr_act()

emngr=eventmngr.eventmngr()
emngr.setconf(conf)

graphics=interface.graphinterface(scr=scr, emngr=emngr, conf=conf)
graphics.draw()
emngr.setGraph(graphics)
fc.updateForecast(conf.deviceconfig.wheatherKey, graphics)

if not conf.homevalues.onoff: #Keep saved configuration state in case of reboot
    graphics.ui_SwitchOnOff.clear_state(lv.STATE.CHECKED)

pointer_c=interface.pointer_cursor(scr=scr)
mouse = evdev.mouse_touch(scr=scr, 
        cursor=pointer_c,
        EVDEV_HOR_MIN=3930, 
        EVDEV_HOR_MAX=236,
        EVDEV_VER_MIN=165, 
        EVDEV_VER_MAX=3929,
        SWAP_AXES=True)

#print(conf.settings.City)

timerClock = lv.timer_create( emngr.clockupdate, 10000, None) 

timerMain = lv.timer_create( realmain,5000,None)

#print(conf.settings.programset[0])

while True:
    time.sleep(100)





