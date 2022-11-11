# LVGL indev driver for evdev mouse device
# (for the unix micropython port)

import ustruct
import select
import lvgl as lv
import time
import sys

# Default crosshair cursor
class crosshair_cursor:
    def __init__(self, scr=None):
        self.scr = scr if scr else lv.scr_act()
        self.hor_res = self.scr.get_width()
        self.ver_res = self.scr.get_height()
        self.cursor_style = lv.style_t()
        self.cursor_style.set_line_width(1)
        self.cursor_style.set_line_dash_gap(5)
        self.cursor_style.set_line_dash_width(1)
        self.cursor_hor = lv.line(self.scr)
        self.cursor_hor.add_style(self.cursor_style, lv.PART.MAIN)
        self.cursor_ver = lv.line(self.scr)
        self.cursor_ver.add_style(self.cursor_style, lv.PART.MAIN)

    def __call__(self, data):
        # print("%d : %d:%d" % (data.state, data.point.x, data.point.y))
        self.cursor_hor.set_points([{'x':0,'y':data.point.y},{'x':self.hor_res,'y':data.point.y}],2)
        self.cursor_ver.set_points([{'y':0,'x':data.point.x},{'y':self.ver_res,'x':data.point.x}],2)

    def delete(self):
        self.cursor_hor.delete()
        self.cursor_ver.delete()

# evdev driver for mouse
class mouse_indev:
    def __init__(self, scr=None, cursor=None, device='/dev/input/mice'):

        # Open evdev and initialize members
        self.evdev = open(device, 'rb')
        self.poll = select.poll()
        self.poll.register(self.evdev.fileno())
        self.scr = scr if scr else lv.scr_act()
        self.cursor = cursor if cursor else crosshair_cursor(self.scr)
        self.hor_res = self.scr.get_width()
        self.ver_res = self.scr.get_height()

        # Register LVGL indev driver
        self.indev_drv = lv.indev_drv_t()
        self.indev_drv.init()
        self.indev_drv.type = lv.INDEV_TYPE.POINTER
        self.indev_drv.read_cb = self.mouse_read
        self.indev = self.indev_drv.register()

    def mouse_read(self, indev_drv, data) -> int:
        
        # Check if there is input to be read from evdev
        if not self.poll.poll()[0][1] & select.POLLIN:
            return 0

        # Read and parse evdev mouse data
        mouse_data = ustruct.unpack('bbb',self.evdev.read(3))

        # Data is relative, update coordinates
        data.point.x += mouse_data[1]
        data.point.y -= mouse_data[2]

        # Handle coordinate overflow cases
        data.point.x = min(data.point.x, self.hor_res - 1)
        data.point.y = min(data.point.y, self.ver_res - 1)
        data.point.x = max(data.point.x, 0)
        data.point.y = max(data.point.y, 0)

        # Update "pressed" status
        data.state = lv.INDEV_STATE.PRESSED if ((mouse_data[0] & 1) == 1) else lv.INDEV_STATE.RELEASED

        # Draw cursor, if needed
        if self.cursor: self.cursor(data)
        return 0

class mouse_touch:
    def __init__(self, scr=None, cursor=None, device='/dev/input/event0',
        format='llHHI',
        EVDEV_HOR_MIN=None, 
        EVDEV_HOR_MAX=None,
        EVDEV_VER_MIN=None, 
        EVDEV_VER_MAX=None,
        SWAP_AXES=False):

        # Open evdev and initialize members
        self.evdev = open(device, 'rb')
        self.poll = select.poll()
        self.poll.register(self.evdev.fileno())
        self.scr = scr if scr else lv.scr_act()
        self.cursor = cursor if cursor else crosshair_cursor(self.scr)
        self.hor_res = self.scr.get_width()
        self.ver_res = self.scr.get_height()
        self.format=format
        self.EVDEV_HOR_MIN = EVDEV_HOR_MIN if EVDEV_HOR_MIN else 0
        self.EVDEV_HOR_MAX = EVDEV_HOR_MAX if EVDEV_HOR_MAX else self.hor_res
        self.EVDEV_VER_MIN = EVDEV_VER_MIN if EVDEV_VER_MIN else 0
        self.EVDEV_VER_MAX = EVDEV_VER_MAX if EVDEV_VER_MAX else self.ver_res
        self.SWAP_AXES = SWAP_AXES

        # Register LVGL indev driver
        self.indev_drv = lv.indev_drv_t()
        self.indev_drv.init()
        self.indev_drv.type = lv.INDEV_TYPE.POINTER
        self.indev_drv.read_cb = self.mouse_read
        self.indev = self.indev_drv.register()
        self.valueRoot_X=0
        self.valueRoot_Y=0
        self.valueRoot_Btn=lv.INDEV_STATE.RELEASED
 

    def mapvalue(self,value_in, in_min, in_max, out_min, out_max):
        mapping = int((value_in - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        return mapping
        

    def mouse_read(self, 
        indev_drv, 
        data) -> int:

        #print(indev_drv)
        #print(indev_drv.type)
        EVENT_SIZE = ustruct.calcsize(self.format)
        EV_ABS          = 0x03
        EV_KEY          = 0x01
        ABS_X           = 0x00
        ABS_Y           = 0x01
        ABS_RX          = 0x03
        ABS_PRESSURE    = 0x18
        ABS_BRAKE       = 0x0a
        ABS_MT_POSITION_X = 0x35    
        ABS_MT_POSITION_Y = 0x36    
        ABS_MT_TRACKING_ID = 0x39
        REL_X              = 0x00
        REL_Y              = 0x01    
        ABS_MAX         = 0x3f
        BTN_TOUCH       = 0x14a
        BTN_MOUSE       = 0x110
        EV_REL          = 0x02
        pressure        = None

        #if self.EVDEV_HOR_MIN is None:
        #    self.EVDEV_HOR_MIN=0
        #if self.EVDEV_VER_MIN is None:
        #    self.EVDEV_VER_MIN=0
        #if self.EVDEV_HOR_MAX is None:
        #    self.EVDEV_HOR_MAX = self.hor_res
        #if self.EVDEV_VER_MAX is None:
        #    self.EVDEV_VER_MAX = self.ver_res

        
        # Check if there is input to be read from evdev
        

        while self.poll.poll()[0][1] & select.POLLIN:
            
            # Read and parse evdev touch data
            (tv_sec, tv_usec, typeval, code, value) = ustruct.unpack(self.format, self.evdev.read(EVENT_SIZE))


            if typeval == EV_REL:
                if code == REL_X:
                    if self.SWAP_AXES is True:
                        self.valueRoot_Y = self.valueRoot_Y + value
                    else:
                        self.valueRoot_X = self.valueRoot_X + value

                if code == REL_Y:
                    if self.SWAP_AXES is True:
                        self.valueRoot_X = self.valueRoot_X + value
                    else:
                        self.valueRoot_Y = self.valueRoot_Y + value
                        
            elif typeval==EV_ABS:
                if code == ABS_X:
                    if self.SWAP_AXES is True:
                        self.valueRoot_Y = value
                    else:
                        self.valueRoot_X = value
                elif code == ABS_Y:
                    if self.SWAP_AXES is True:
                        self.valueRoot_X = value
                    else:
                        self.valueRoot_Y = value
                elif code == ABS_MT_POSITION_X:
                    if self.SWAP_AXES is True:
                        self.valueRoot_Y = value
                    else:
                        self.valueRoot_X = value

                elif code == ABS_MT_POSITION_Y:
                    if self.SWAP_AXES is True:
                        self.valueRoot_X = value
                    else:
                        self.valueRoot_Y = value

                elif code == ABS_MT_TRACKING_ID:
                    if value == -1:
                        self.valueRoot_Btn = lv.INDEV_STATE.RELEASED
                    elif value == 0:
                        self.valueRoot_Btn = lv.INDEV_STATE.PRESSED
            elif typeval == EV_KEY:
                if code == BTN_TOUCH or code == BTN_MOUSE:
                    if value == 0:
                        self.valueRoot_Btn = lv.INDEV_STATE.RELEASED
                    elif value == 1:
                        self.valueRoot_Btn = lv.INDEV_STATE.PRESSED
        
        data.point.y = self.mapvalue(self.valueRoot_Y, self.EVDEV_VER_MIN, self.EVDEV_VER_MAX, 0, self.scr.get_height())
        data.point.x = self.mapvalue(self.valueRoot_X, self.EVDEV_HOR_MIN, self.EVDEV_HOR_MAX, 0, self.scr.get_width())
        data.state = self.valueRoot_Btn

        if data.point.x < 0:
            data.point.x == 0
        if data.point.y < 0:
            data.point.y == 0
        if data.point.x > self.scr.get_width():
            data.point.x = self.scr.get_width()-1
        if data.point.y > self.scr.get_height():
            data.point.y = self.scr.get_height()-1


        if self.cursor: self.cursor(data)
        return 0


    

    def delete(self):
        self.evdev.close()
        if self.cursor and hasattr(self.cursor, 'delete'):
            self.cursor.delete()
        self.indev.enable(False)
