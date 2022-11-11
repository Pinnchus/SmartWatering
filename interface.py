import lvgl as lv
import evdev


class pointer_cursor:
    def __init__(self, scr=None):
        self.scr = scr if scr else lv.scr_act()
        self.img = lv.img(self.scr)
        self.img.set_src(lv.SYMBOL.GPS)
        self.cursor_style = lv.style_t()
        self.cursor_img = self.img

    def __call__(self, data):
        # print("State: %d - ValorX: %d  ValorY:%d" % (data.state, data.point.x, data.point.y))
        self.cursor_img.set_pos(data.point.x - 15, data.point.y)

    def delete(self):
        self.cursor_hor.delete()
        self.cursor_ver.delete()


class graphinterface:
    def __init__(self, scr=None, emngr=None, conf=None):
        self.scr = scr if scr else lv.scr_act()
        self.conf = conf if conf else None
        self.emngr = emngr if emngr else None
        self.maintab = None
        self.ui_Label1HoraActual = None
        self.ui_LabelStatus = None
        self.ui_LabelTempActual = None
        self.style_line = None
        self.line1 = None
        self.ui_LabelMode = None
        self.ui_LabelRunningTime = None
        self.ui_LabelDelayed = None
        self.ui_DropdownMode = None
        self.ui_RUN = None
        self.ui_LabelRUN = None
        self.ui_RolManRunTime = None
        self.ui_RolManDelay = None
        self.ui_Label2 = None
        self.style_radio = None
        self.style_radio_chk = None
        self.ui_ChBoxZona8 = None
        self.ui_ChBoxZona1 = None
        self.ui_ChBoxZona2 = None
        self.ui_ChBoxZona3 = None
        self.ui_ChBoxZona4 = None
        self.ui_ChBoxZona5 = None
        self.ui_ChBoxZona6 = None
        self.ui_ChBoxZona7 = None
        self.lblobjtemp = [None, None, None, None, None, None, None, None]
        self.ui_SwitchOnOff = None
        self.ui_LabelOnOff = None
        self.ui_ButtonWifi = None
        self.ui_LabelWifi = None
        self.ui_WeatherSw = None
        self.ui_LabelWeatherSw = None
        self.ui_SmartSw = None
        self.ui_LabelSmartSw = None
        self.ui_SensorSw = None
        self.ui_LabelSensorSw = None
        self.ui_BtnMeasures = None
        self.ui_lblMeasures = None
        self.ui_Tab2Label_HOY = None
        self.ui_Tab2Label_Manana = None
        self.ui_Tab2Label_P_Manana = None
        self.ui_Tab2FCImg1 = None
        self.ui_Tab2FCImg2 = None
        self.ui_Tab2FCImg3 = None
        self.ui_ChBoxDays1 = None
        self.ui_ChBoxDays2 = None
        self.ui_ChBoxDays3 = None
        self.ui_ChBoxDays4 = None
        self.ui_ChBoxDays5 = None
        self.ui_ChBoxDays6 = None
        self.ui_ChBoxDays7 = None
        self.ui_ChBoxMatrix = [None, None, None, None, None, None, None]
        self.ui_ChBoxMatrixPositionsX = [103, 148, 193, 238, 283, 328, 372]
        self.ui_Tab3lblRunningDays = None
        self.ui_Tab3lblPrgrm = None
        self.ui_Tab3lblStartTime = None
        self.ui_Tab3lblZone = None
        self.ui_Tab3lblRunningT = None
        self.ui_Tab3RollerPgm = None
        self.ui_Tab3RollerTimeH = None
        self.ui_Tab3RollerTimeM = None
        self.ui_Tab3RollerZone = None
        self.ui_Tab3RollRunningTime = None
        self.ui_Tab3lblCountry = None
        self.ui_Tab3lblCity = None
        self.ui_Tab3DdownGMT = None
        self.ui_Tab3lblWIFI = None
        self.ui_Tab3TextAreaSSID = None
        self.ui_Tab3TextAreaWifiKEY = None
        self.ui_Tab3lblSENSORS = None
        self.ui_Tab3DdownSENSORS = None
        self.ui_Tab3TxtArSensrorName = None
        self.ui_Tab3TxtArSensrorIP = None
        self.ui_Tab3BtnReboot = None
        self.ui_Tab3lblbtnReboot = None
        self.ui_Tab3ButtonApply = None
        self.ui_Tab3lblApply = None
        self.ui_Tab3ButtonCancel = None
        self.ui_Tab3lblCancel = None
        self.configuredtime = ["Mode Automatic"]
        self.configuredtime_manual = [
            "1 Minute",
            "2 Minutes",
            "3 Minutes",
            "4 Minutes",
            "5 Minutes",
            "6 Minutes",
            "7 Minutes",
            "8 Minutes",
            "9 Minutes",
            "10 Minutes",
            "11 Minutes",
            "12 Minutes",
            "13 Minutes",
            "14 Minutes",
            "15 Minutes",
            "20 Minutes",
            "25 Minutes",
            "30 Minutes",
            "35 Minutes",
            "40 Minutes",
            "45 Minutes",
            "50 Minutes",
            "55 Minutes",
            "60 Minutes",
        ]
        self.configuredtime_program = [
            "Program 0",
            "Program 1",
            "Program 2",
            "Program 3",
            "Program 4",
            "Program 5",
            "Program 6",
            "Program 7",
            "Program 8",
            "Program 9",
            "Program 10",
            "Program 11",
            "Program 12",
            "Program 13",
            "Program 14",
            "Program 15",
        ]
        self.delaytime = [
            "Now",
            "1 Minute",
            "2 Minutes",
            "5 Minutes",
            "10 Minutes",
            "15 Minutes",
            "20 Minutes",
            "25 Minutes",
            "30 Minutes",
            "35 Minutes",
            "40 Minutes",
            "45 Minutes",
            "50 Minutes",
            "55 Minutes",
            "60 Minutes",
        ]

        self.modeval = [
            "Automatic",
            "Pgrm Delayed",
            "Zones & Time",
            "Pgrm To Off",
            "Zones & Time Off",
        ]

    def draw(self):
        self.maintab = lv.tabview(self.scr, lv.DIR.TOP, 45)
        self.tab1 = self.maintab.add_tab("HOME")
        self.tab1.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self.tab1.clear_flag(lv.obj.FLAG.SCROLLABLE)

        self.tab2 = self.maintab.add_tab("FORECAST")
        self.tab2.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        self.tab2.clear_flag(lv.obj.FLAG.SCROLLABLE)

        self.tab3 = self.maintab.add_tab("SETTINGS")
        self.tab3.set_scrollbar_mode(lv.SCROLLBAR_MODE.ON)
        self.tab3.set_scroll_dir(lv.DIR.VER)

        #####################TAB HOME################
        # TAB BORDERS 15,60
        self.ui_Label1HoraActual = lv.label(self.tab1)
        self.ui_Label1HoraActual.set_width(130)
        self.ui_Label1HoraActual.set_height(45)
        self.ui_Label1HoraActual.set_pos(10, 0)
        self.ui_Label1HoraActual.set_text("20:30")
        self.ui_Label1HoraActual.set_style_text_font(lv.font_montserrat_20, 0)
        self.ui_Label1HoraActual.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

        self.ui_LabelStatus = lv.label(self.tab1)
        self.ui_LabelStatus.set_width(130)
        self.ui_LabelStatus.set_height(45)
        self.ui_LabelStatus.set_pos(175, 0)
        self.ui_LabelStatus.set_text("Status")
        self.ui_LabelStatus.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelStatus.set_style_text_font(lv.font_montserrat_20, 0)

        self.ui_LabelTempActual = lv.label(self.tab1)
        self.ui_LabelTempActual.set_width(130)
        self.ui_LabelTempActual.set_height(45)
        self.ui_LabelTempActual.set_pos(325, 0)
        self.ui_LabelTempActual.set_text("10C - 55%")
        self.ui_LabelTempActual.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelTempActual.set_style_text_font(lv.font_montserrat_20, 0)

        line_points = [{"x": 0, "y": 30}, {"x": 450, "y": 30}]
        self.style_line = lv.style_t()
        self.style_line.init()
        self.style_line.set_line_width(2)
        self.style_line.set_line_color(lv.palette_main(lv.PALETTE.BLUE))
        self.style_line.set_line_rounded(True)
        # Create a line and apply the new style
        self.line1 = lv.line(self.tab1)
        self.line1.add_style(self.style_line, 0)
        self.line1.set_points(line_points, 2)  # Set the points

        self.ui_LabelMode = lv.label(self.tab1)
        self.ui_LabelMode.set_width(68)
        self.ui_LabelMode.set_height(23)
        self.ui_LabelMode.set_pos(50, 35)
        self.ui_LabelMode.set_text("Mode")
        self.ui_LabelMode.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_LabelMode.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelMode.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_LabelRunningTime = lv.label(self.tab1)
        self.ui_LabelRunningTime.set_width(130)
        self.ui_LabelRunningTime.set_height(23)
        self.ui_LabelRunningTime.set_pos(178, 35)
        self.ui_LabelRunningTime.set_text("Runnig Time")
        self.ui_LabelRunningTime.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_LabelRunningTime.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelRunningTime.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_LabelDelayed = lv.label(self.tab1)
        self.ui_LabelDelayed.set_width(78)
        self.ui_LabelDelayed.set_height(23)
        self.ui_LabelDelayed.set_pos(350, 35)
        self.ui_LabelDelayed.set_text("Delayed")
        self.ui_LabelDelayed.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_LabelDelayed.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelDelayed.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_DropdownMode = lv.dropdown(self.tab1)
        self.ui_DropdownMode.set_options("\n".join(self.modeval))
        self.ui_DropdownMode.set_width(160)
        self.ui_DropdownMode.set_height(42)
        self.ui_DropdownMode.set_pos(4, 58)
        self.ui_DropdownMode.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_DropdownMode.set_style_text_align(lv.TEXT_ALIGN.AUTO, 0)
        self.ui_DropdownMode.add_event_cb(
            self.emngr.ui_DropdownMode_evt_hndlr, lv.EVENT.ALL, None
        )
        self.ui_RUN = lv.btn(self.tab1)
        self.ui_RUN.set_width(160)
        self.ui_RUN.set_height(35)
        self.ui_RUN.set_pos(4, 107)
        self.ui_RUN.add_event_cb(self.emngr.ui_RUN_evt_hndlr, lv.EVENT.ALL, None)
        self.ui_LabelRUN = lv.label(self.ui_RUN)
        self.ui_LabelRUN.set_width(lv.SIZE_CONTENT)
        self.ui_LabelRUN.set_height(lv.SIZE_CONTENT)
        self.ui_LabelRUN.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_LabelRUN.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelRUN.set_style_text_font(lv.font_montserrat_18, 0)
        self.ui_LabelRUN.set_text(lv.SYMBOL.PLAY)

        self.ui_RolManRunTime = lv.roller(self.tab1)
        self.ui_RolManRunTime.set_options(
            "\n".join(self.configuredtime), lv.roller.MODE.INFINITE
        )
        self.ui_RolManRunTime.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_RolManRunTime.set_width(130)
        self.ui_RolManRunTime.set_height(85)
        self.ui_RolManRunTime.set_pos(178, 58)

        self.ui_RolManDelay = lv.roller(self.tab1)
        self.ui_RolManDelay.set_options(
            "\n".join(self.delaytime), lv.roller.MODE.INFINITE
        )
        self.ui_RolManDelay.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_RolManDelay.set_width(130)
        self.ui_RolManDelay.set_height(85)
        self.ui_RolManDelay.set_pos(323, 58)

        self.ui_Label2 = lv.label(self.tab1)
        self.ui_Label2.set_width(102)
        self.ui_Label2.set_height(lv.SIZE_CONTENT)
        self.ui_Label2.set_pos(0, 165)
        self.ui_Label2.set_text("Enable Zones")
        self.ui_Label2.clear_flag(lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE)
        self.ui_Label2.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Label2.set_style_text_font(lv.font_montserrat_14, 0)

        ####Format Checkbox
        self.style_radio = lv.style_t()
        self.style_radio.init()
        self.style_radio.set_radius(lv.RADIUS_CIRCLE)
        self.style_radio_chk = lv.style_t()
        self.style_radio_chk.init()
        self.style_radio_chk.set_bg_img_src(None)
        ####END Format Checkbox

        self.ui_ChBoxZona8 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona8.set_text("")
        self.ui_ChBoxZona8.set_width(20)
        self.ui_ChBoxZona8.set_height(20)
        self.ui_ChBoxZona8.set_pos(421, 165)
        self.ui_ChBoxZona8.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona8.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona8.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        self.ui_ChBoxZona1 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona1.set_text("")
        self.ui_ChBoxZona1.set_width(20)
        self.ui_ChBoxZona1.set_height(20)
        self.ui_ChBoxZona1.set_pos(103, 165)
        self.ui_ChBoxZona1.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona1.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona1.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        self.ui_ChBoxZona2 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona2.set_text("")
        self.ui_ChBoxZona2.set_width(20)
        self.ui_ChBoxZona2.set_height(20)
        self.ui_ChBoxZona2.set_pos(149, 165)
        self.ui_ChBoxZona2.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona2.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona2.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        self.ui_ChBoxZona3 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona3.set_text("")
        self.ui_ChBoxZona3.set_width(20)
        self.ui_ChBoxZona3.set_height(20)
        self.ui_ChBoxZona3.set_pos(195, 165)
        self.ui_ChBoxZona3.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona3.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona3.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        self.ui_ChBoxZona4 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona4.set_text("")
        self.ui_ChBoxZona4.set_width(20)
        self.ui_ChBoxZona4.set_height(20)
        self.ui_ChBoxZona4.set_pos(240, 165)
        self.ui_ChBoxZona4.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona4.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona4.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        self.ui_ChBoxZona5 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona5.set_text("")
        self.ui_ChBoxZona5.set_width(20)
        self.ui_ChBoxZona5.set_height(20)
        self.ui_ChBoxZona5.set_pos(286, 165)
        self.ui_ChBoxZona5.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona5.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona5.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        self.ui_ChBoxZona6 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona6.set_text("")
        self.ui_ChBoxZona6.set_width(20)
        self.ui_ChBoxZona6.set_height(20)
        self.ui_ChBoxZona6.set_pos(331, 165)
        self.ui_ChBoxZona6.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona6.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona6.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        self.ui_ChBoxZona7 = lv.checkbox(self.tab1)
        self.ui_ChBoxZona7.set_text("")
        self.ui_ChBoxZona7.set_width(20)
        self.ui_ChBoxZona7.set_height(20)
        self.ui_ChBoxZona7.set_pos(377, 165)
        self.ui_ChBoxZona7.add_flag(lv.obj.FLAG.EVENT_BUBBLE)
        self.ui_ChBoxZona7.add_style(self.style_radio, lv.PART.INDICATOR)
        self.ui_ChBoxZona7.add_style(
            self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
        )

        # Set Checkbox & Rollers Start State
        self.ui_RolManRunTime.add_state(lv.STATE.DISABLED)
        self.ui_RolManDelay.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona1.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona2.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona3.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona4.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona5.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona6.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona7.add_state(lv.STATE.DISABLED)
        self.ui_ChBoxZona8.add_state(lv.STATE.DISABLED)

        #####Print Labes for Checkbox Zones
        positionsLabelsCheckbox = [110, 156, 201, 245, 292, 336, 383, 426]
        for i in range(1, 9):
            # print(i)
            # print(positions[i-1])
            self.lblobjtemp[i - 1] = lv.label(self.tab1)
            self.lblobjtemp[i - 1].set_width(lv.SIZE_CONTENT)
            self.lblobjtemp[i - 1].set_height(lv.SIZE_CONTENT)
            self.lblobjtemp[i - 1].set_y(150)
            self.lblobjtemp[i - 1].set_x(positionsLabelsCheckbox[i - 1])  # 110,156,201
            texttemp = str(i)
            # print(texttemp)
            self.lblobjtemp[i - 1].set_text(texttemp)
            self.lblobjtemp[i - 1].clear_flag(
                lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
            )
            self.lblobjtemp[i - 1].set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            self.lblobjtemp[i - 1].set_style_text_font(lv.font_montserrat_14, 0)
        #####END Print Labes for Checkbox Zones

        self.ui_SwitchOnOff = lv.switch(self.tab1)
        self.ui_SwitchOnOff.set_width(80)
        self.ui_SwitchOnOff.set_height(40)
        self.ui_SwitchOnOff.set_pos(4, 215)
        self.ui_SwitchOnOff.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_SwitchOnOff.add_state(lv.STATE.CHECKED)
        self.ui_LabelOnOff = lv.label(self.tab1)
        self.ui_LabelOnOff.set_width(lv.SIZE_CONTENT)
        self.ui_LabelOnOff.set_height(lv.SIZE_CONTENT)
        self.ui_LabelOnOff.set_pos(17, 195)
        self.ui_LabelOnOff.set_text("ON-OFF")
        self.ui_LabelOnOff.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_LabelOnOff.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelOnOff.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_ButtonWifi = lv.btn(self.tab1)
        self.ui_ButtonWifi.set_width(30)
        self.ui_ButtonWifi.set_height(30)
        self.ui_ButtonWifi.set_pos(430, 225)
        self.ui_ButtonWifi.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_ButtonWifi.set_style_radius(lv.RADIUS_CIRCLE, 0)
        self.ui_LabelWifi = lv.label(self.ui_ButtonWifi)
        self.ui_LabelWifi.set_width(lv.SIZE_CONTENT)
        self.ui_LabelWifi.set_height(lv.SIZE_CONTENT)
        self.ui_LabelWifi.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_LabelWifi.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelWifi.set_style_text_font(lv.font_montserrat_18, 0)
        self.ui_LabelWifi.set_text(lv.SYMBOL.WIFI)

        self.ui_WeatherSw = lv.switch(self.tab1)
        self.ui_WeatherSw.set_width(70)
        self.ui_WeatherSw.set_height(30)
        self.ui_WeatherSw.set_pos(346, 225)
        self.ui_WeatherSw.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_LabelWeatherSw = lv.label(self.tab1)
        self.ui_LabelWeatherSw.set_width(lv.SIZE_CONTENT)
        self.ui_LabelWeatherSw.set_height(lv.SIZE_CONTENT)
        self.ui_LabelWeatherSw.set_pos(346, 200)
        self.ui_LabelWeatherSw.set_text("Weather")
        self.ui_LabelWeatherSw.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_LabelWeatherSw.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelWeatherSw.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_SmartSw = lv.switch(self.tab1)
        self.ui_SmartSw.set_width(70)
        self.ui_SmartSw.set_height(30)
        self.ui_SmartSw.set_pos(260, 225)
        self.ui_SmartSw.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_LabelSmartSw = lv.label(self.tab1)
        self.ui_LabelSmartSw.set_width(lv.SIZE_CONTENT)
        self.ui_LabelSmartSw.set_height(lv.SIZE_CONTENT)
        self.ui_LabelSmartSw.set_pos(275, 200)
        self.ui_LabelSmartSw.set_text("Smart")
        self.ui_LabelSmartSw.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_LabelSmartSw.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelSmartSw.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_SensorSw = lv.switch(self.tab1)
        self.ui_SensorSw.set_width(70)
        self.ui_SensorSw.set_height(30)
        self.ui_SensorSw.set_pos(175, 225)
        self.ui_SensorSw.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_LabelSensorSw = lv.label(self.tab1)
        self.ui_LabelSensorSw.set_width(lv.SIZE_CONTENT)
        self.ui_LabelSensorSw.set_height(lv.SIZE_CONTENT)
        self.ui_LabelSensorSw.set_pos(180, 200)
        self.ui_LabelSensorSw.set_text("Sensors")
        self.ui_LabelSensorSw.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_LabelSensorSw.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelSensorSw.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_BtnMeasures = lv.btn(self.tab1)
        self.ui_BtnMeasures.set_width(30)
        self.ui_BtnMeasures.set_height(30)
        self.ui_BtnMeasures.set_pos(117, 225)
        self.ui_BtnMeasures.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_BtnMeasures.set_style_radius(lv.RADIUS_CIRCLE, 0)
        self.ui_lblMeasures = lv.label(self.tab1)
        self.ui_lblMeasures.set_width(lv.SIZE_CONTENT)
        self.ui_lblMeasures.set_height(lv.SIZE_CONTENT)
        self.ui_lblMeasures.set_pos(102, 200)
        self.ui_lblMeasures.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_lblMeasures.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_lblMeasures.set_text("Measures")

        #####################END TAB HOME################

        #####################TAB FORECAST################

        self.ui_Tab2Label_HOY = lv.label(self.tab2)
        self.ui_Tab2Label_HOY.set_width(310)
        self.ui_Tab2Label_HOY.set_height(72)
        self.ui_Tab2Label_HOY.set_pos(160, 5)
        self.ui_Tab2Label_HOY.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        self.ui_Tab2Label_HOY.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab2Label_HOY.set_text("Hoy")
        self.ui_Tab2Label_HOY.set_style_border_color(
            lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab2Label_HOY.set_style_border_width(1, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ui_Tab2Label_HOY.set_style_border_side(
            lv.BORDER_SIDE.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT
        )

        self.ui_Tab2Label_Manana = lv.label(self.tab2)
        self.ui_Tab2Label_Manana.set_width(310)
        self.ui_Tab2Label_Manana.set_height(72)
        self.ui_Tab2Label_Manana.set_pos(160, 87)
        self.ui_Tab2Label_Manana.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        self.ui_Tab2Label_Manana.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab2Label_Manana.set_text("Manana")
        self.ui_Tab2Label_Manana.set_style_border_color(
            lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab2Label_Manana.set_style_border_width(
            1, lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab2Label_Manana.set_style_border_side(
            lv.BORDER_SIDE.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT
        )

        self.ui_Tab2Label_P_Manana = lv.label(self.tab2)
        self.ui_Tab2Label_P_Manana.set_width(310)
        self.ui_Tab2Label_P_Manana.set_height(72)
        self.ui_Tab2Label_P_Manana.set_pos(160, 172)
        self.ui_Tab2Label_P_Manana.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        self.ui_Tab2Label_P_Manana.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab2Label_P_Manana.set_text("Pasado Manana")
        self.ui_Tab2Label_P_Manana.set_style_border_color(
            lv.color_hex(0x000000), lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab2Label_P_Manana.set_style_border_width(
            1, lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab2Label_P_Manana.set_style_border_side(
            lv.BORDER_SIDE.LEFT, lv.PART.MAIN | lv.STATE.DEFAULT
        )

        self.ui_Tab2FCImg1 = lv.img(self.tab2)
        self.ui_Tab2FCImg1.set_width(100)
        self.ui_Tab2FCImg1.set_height(100)
        self.ui_Tab2FCImg1.set_pos(20, 5)

        self.ui_Tab2FCImg2 = lv.img(self.tab2)
        self.ui_Tab2FCImg2.set_width(100)
        self.ui_Tab2FCImg2.set_height(100)
        self.ui_Tab2FCImg2.set_pos(20, 87)

        self.ui_Tab2FCImg3 = lv.img(self.tab2)
        self.ui_Tab2FCImg3.set_width(100)
        self.ui_Tab2FCImg3.set_height(100)
        self.ui_Tab2FCImg3.set_pos(20, 172)

        #####################END TAB FORECAST################

        ##################### TAB SETTINGS ################

        self.ui_Tab3lblPrgrm = lv.label(self.tab3)
        self.ui_Tab3lblPrgrm.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblPrgrm.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblPrgrm.set_pos(2, 0)
        self.ui_Tab3lblPrgrm.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblPrgrm.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_Tab3lblPrgrm.set_style_text_font(lv.font_montserrat_22, 0)
        self.ui_Tab3lblPrgrm.set_text("Program")

        self.ui_Tab3lblStartTime = lv.label(self.tab3)
        self.ui_Tab3lblStartTime.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblStartTime.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblStartTime.set_pos(111, 0)
        self.ui_Tab3lblStartTime.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblStartTime.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_Tab3lblStartTime.set_style_text_font(lv.font_montserrat_22, 0)
        self.ui_Tab3lblStartTime.set_text("StartTime")

        self.ui_Tab3lblZone = lv.label(self.tab3)
        self.ui_Tab3lblZone.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblZone.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblZone.set_pos(250, 0)
        self.ui_Tab3lblZone.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblZone.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_Tab3lblZone.set_style_text_font(lv.font_montserrat_22, 0)
        self.ui_Tab3lblZone.set_text("Zone")

        self.ui_Tab3lblRunningT = lv.label(self.tab3)
        self.ui_Tab3lblRunningT.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblRunningT.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblRunningT.set_pos(353, 0)
        self.ui_Tab3lblRunningT.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblRunningT.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_Tab3lblRunningT.set_style_text_font(lv.font_montserrat_22, 0)
        self.ui_Tab3lblRunningT.set_text("Running")

        self.ui_Tab3RollerPgm = lv.roller(self.tab3)
        self.ui_Tab3RollerPgm.set_options(
            "\n".join(
                [
                    "Program 0",
                    "Program 1",
                    "Program 2",
                    "Program 3",
                    "Program 4",
                    "Program 5",
                    "Program 6",
                    "Program 7",
                    "Program 8",
                    "Program 9",
                    "Program 10",
                    "Program 11",
                    "Program 12",
                    "Program 13",
                    "Program 14",
                    "Program 15",
                ]
            ),
            lv.roller.MODE.INFINITE,
        )
        self.ui_Tab3RollerPgm.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab3RollerPgm.set_width(108)
        self.ui_Tab3RollerPgm.set_height(80)
        self.ui_Tab3RollerPgm.set_pos(0, 25)
        self.ui_Tab3RollerPgm.add_event_cb(self.emngr.ui_Tab3RollerPgm_evt_hndlr, lv.EVENT.ALL, None)
        self.emngr.currentProgram=self.ui_Tab3RollerPgm.get_selected()


        self.ui_Tab3RollerTimeH = lv.roller(self.tab3)
        self.ui_Tab3RollerTimeH.set_options(
            "\n".join(
                [
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "OFF",
                ]
            ),
            lv.roller.MODE.INFINITE,
        )
        self.ui_Tab3RollerTimeH.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab3RollerTimeH.set_width(50)
        self.ui_Tab3RollerTimeH.set_height(80)
        self.ui_Tab3RollerTimeH.set_pos(116, 25)
        self.ui_Tab3RollerTimeH.set_selected(
            self.conf.settings.programset[self.ui_Tab3RollerPgm.get_selected()][0][0],
            lv.ANIM.OFF,
        )
        self.ui_Tab3RollerTimeH.add_event_cb(self.emngr.ui_Tab3RollerTimeH_evt_hndlr, lv.EVENT.ALL, None)

        self.ui_Tab3RollerTimeM = lv.roller(self.tab3)
        self.ui_Tab3RollerTimeM.set_options(
            "\n".join(
                [
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                    "32",
                    "33",
                    "34",
                    "35",
                    "36",
                    "37",
                    "38",
                    "39",
                    "40",
                    "41",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                    "55",
                    "56",
                    "57",
                    "58",
                    "59",
                ]
            ),
            lv.roller.MODE.INFINITE,
        )
        self.ui_Tab3RollerTimeM.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab3RollerTimeM.set_width(50)
        self.ui_Tab3RollerTimeM.set_height(80)
        self.ui_Tab3RollerTimeM.set_pos(170, 25)
        self.ui_Tab3RollerTimeM.set_selected(
            self.conf.settings.programset[self.ui_Tab3RollerPgm.get_selected()][0][1],
            lv.ANIM.OFF,
        )
        self.ui_Tab3RollerTimeM.add_event_cb(self.emngr.ui_Tab3RollerTimeM_evt_hndlr, lv.EVENT.ALL, None)



        self.ui_Tab3RollerZone = lv.roller(self.tab3)
        self.ui_Tab3RollerZone.set_options(
            "\n".join(
                [
                    "Zone 1",
                    "Zone 2",
                    "Zone 3",
                    "Zone 4",
                    "Zone 5",
                    "Zone 6",
                    "Zone 7",
                    "Zone 8",
                ]
            ),
            lv.roller.MODE.INFINITE,
        )
        self.ui_Tab3RollerZone.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab3RollerZone.set_width(108)
        self.ui_Tab3RollerZone.set_height(80)
        self.ui_Tab3RollerZone.set_pos(230, 25)
        self.ui_Tab3RollerZone.add_event_cb(self.emngr.ui_Tab3RollerZone_evt_hndlr, lv.EVENT.ALL, None)


        self.ui_Tab3RollRunningTime = lv.roller(self.tab3)
        self.ui_Tab3RollRunningTime.set_options(
            "\n".join(
                [
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                    "32",
                    "33",
                    "34",
                    "35",
                    "36",
                    "37",
                    "38",
                    "39",
                    "40",
                    "41",
                    "42",
                    "43",
                    "44",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "51",
                    "52",
                    "53",
                    "54",
                    "55",
                    "56",
                    "57",
                    "58",
                    "59",
                ]
            ),
            lv.roller.MODE.INFINITE,
        )
        self.ui_Tab3RollRunningTime.set_style_text_font(lv.font_montserrat_14, 0)
        self.ui_Tab3RollRunningTime.set_width(108)
        self.ui_Tab3RollRunningTime.set_height(80)
        self.ui_Tab3RollRunningTime.set_pos(350, 25)
        self.ui_Tab3RollRunningTime.set_selected(
            self.conf.settings.programset[self.ui_Tab3RollerPgm.get_selected()][1][
                self.ui_Tab3RollerZone.get_selected()
            ],
            lv.ANIM.OFF,
        )
        self.ui_Tab3RollRunningTime.add_event_cb(self.emngr.ui_Tab3RollRunningTime_evt_hndlr, lv.EVENT.ALL, None)

        if (
            self.conf.settings.programset[self.ui_Tab3RollerPgm.get_selected()][0][0]
            == 24
        ):  # 24 is OFF
            self.ui_Tab3RollerTimeM.add_state(lv.STATE.DISABLED)
            self.ui_Tab3RollerZone.add_state(lv.STATE.DISABLED)
            self.ui_Tab3RollRunningTime.add_state(lv.STATE.DISABLED)

        else:
            self.ui_Tab3RollerTimeM.clear_state(lv.STATE.DISABLED)
            self.ui_Tab3RollerZone.clear_state(lv.STATE.DISABLED)
            self.ui_Tab3RollRunningTime.clear_state(lv.STATE.DISABLED)

        ##############Days Checkbox ######################

        for i in range(7):
            self.ui_ChBoxMatrix[i] = lv.checkbox(self.tab3)
            self.ui_ChBoxMatrix[i].set_width(20)
            self.ui_ChBoxMatrix[i].set_height(20)
            self.ui_ChBoxMatrix[i].set_pos(self.ui_ChBoxMatrixPositionsX[i], 135)
            self.ui_ChBoxMatrix[i].add_flag(
                lv.obj.FLAG.EVENT_BUBBLE | lv.obj.FLAG.SCROLL_ON_FOCUS
            )
            self.ui_ChBoxMatrix[i].add_style(self.style_radio, lv.PART.INDICATOR)
            self.ui_ChBoxMatrix[i].add_style(
                self.style_radio_chk, lv.PART.INDICATOR | lv.STATE.CHECKED
            )
            self.ui_ChBoxMatrix[i].add_event_cb(self.emngr.ui_ChBoxMatrix_evt_hndlr, lv.EVENT.ALL, None)

            if (
                self.conf.settings.programset[self.ui_Tab3RollerPgm.get_selected()][2][
                    i
                ]
                == 0
            ):
                self.ui_ChBoxMatrix[i].clear_state(lv.STATE.CHECKED)
            else:
                self.ui_ChBoxMatrix[i].add_state(lv.STATE.CHECKED)
            if self.ui_Tab3RollerTimeH.get_selected() == 24:  # 24 is Off position
                self.ui_ChBoxMatrix[i].add_state(lv.STATE.DISABLED)
            else:
                self.ui_ChBoxMatrix[i].clear_state(lv.STATE.DISABLED)

        #####Print Labes for Checkbox Config
        positionsLabelsCheckbox = [106, 151, 196, 241, 286, 331, 376]
        positionsLabelDays = ["L", "M", "M", "J", "V", "S", "D"]
        for i in range(7):
            # print(i)
            # print(positions[i-1])
            self.objtemp = lv.label(self.tab3)
            self.objtemp.set_width(lv.SIZE_CONTENT)
            self.objtemp.set_height(lv.SIZE_CONTENT)
            self.objtemp.set_y(115)
            self.objtemp.set_x(positionsLabelsCheckbox[i])  # 110,156,201
            # texttemp=positionsLabelDays[i]
            # print(texttemp)
            self.objtemp.set_text(positionsLabelDays[i])
            self.objtemp.clear_flag(
                lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
            )
            self.objtemp.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
            self.objtemp.set_style_text_font(lv.font_montserrat_14, 0)
        #####END Print Labes for Checkbox Config

        self.ui_Tab3lblRunningDays = lv.label(self.tab3)
        self.ui_Tab3lblRunningDays.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblRunningDays.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblRunningDays.set_pos(0, 125)
        self.ui_Tab3lblRunningDays.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblRunningDays.set_style_text_font(lv.font_montserrat_16, 0)
        self.ui_Tab3lblRunningDays.set_text("Running\nDays")
        # END Days Checbox
        #Country Refresh Selector

        self.ui_CityRefresh = lv.btn(self.tab3)
        self.ui_CityRefresh.set_width(35)
        self.ui_CityRefresh.set_height(35)
        self.ui_CityRefresh.set_pos(0, 170)
        self.ui_CityRefresh.clear_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_CityRefresh.set_style_radius(lv.RADIUS_CIRCLE, 0)
        self.ui_LabelCityRefresh = lv.label(self.ui_CityRefresh)
        self.ui_LabelCityRefresh.set_width(lv.SIZE_CONTENT)
        self.ui_LabelCityRefresh.set_height(lv.SIZE_CONTENT)
        self.ui_LabelCityRefresh.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_LabelCityRefresh.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_LabelCityRefresh.set_style_text_font(lv.font_montserrat_18, 0)
        self.ui_LabelCityRefresh.set_text(lv.SYMBOL.REFRESH)
        self.ui_CityRefresh.add_event_cb(self.emngr.getGeoLocatio_evt_hndlr, lv.EVENT.ALL, None)

        self.ui_Tab3BCountry = lv.btn(self.tab3)
        self.ui_Tab3BCountry.set_width(135)
        self.ui_Tab3BCountry.set_height(30)
        self.ui_Tab3BCountry.set_pos(40, 173)
        self.ui_Tab3BCountry.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_Tab3BCountry.add_state(lv.STATE.DISABLED)
        self.ui_Tab3lblCountry = lv.label(self.ui_Tab3BCountry)
        self.ui_Tab3lblCountry.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblCountry.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblCountry.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_Tab3lblCountry.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblCountry.set_style_text_font(lv.font_montserrat_16, 0)
        temporalText=self.conf.settings.Country+", "+self.conf.settings.CountryCode
        self.ui_Tab3lblCountry.set_text(temporalText)
        

        self.ui_Tab3BCity = lv.btn(self.tab3)
        self.ui_Tab3BCity.set_width(178)
        self.ui_Tab3BCity.set_height(30)
        self.ui_Tab3BCity.set_pos(180, 173)
        self.ui_Tab3BCity.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_Tab3BCity.add_state(lv.STATE.DISABLED)
        self.ui_Tab3lblCity = lv.label(self.ui_Tab3BCity)
        self.ui_Tab3lblCity.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblCity.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblCity.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_Tab3lblCity.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblCity.set_style_text_font(lv.font_montserrat_16, 0)
        temporalText=self.conf.settings.City
        self.ui_Tab3lblCity.set_text(temporalText)

        self.ui_Tab3DdownGMT = lv.dropdown(self.tab3)
        self.ui_Tab3DdownGMT.set_options(
            "\n".join(
                [
                    "GMT",
                    "-12",
                    "-11",
                    "-10",
                    "-9",
                    "-8",
                    "-7",
                    "-6",
                    "-5",
                    "-4",
                    "-3",
                    "-2",
                    "-1",
                    "+0",
                    "+1",
                    "+2",
                    "+3",
                    "+4",
                    "+5",
                    "+6",
                    "+7",
                    "+8",
                    "+9",
                    "+10",
                    "+11",
                    "+12",
                    "+13",
                ]
            )
        )
        self.ui_Tab3DdownGMT.set_width(95)
        self.ui_Tab3DdownGMT.set_height(30)
        self.ui_Tab3DdownGMT.set_pos(360, 173)
        self.ui_Tab3DdownGMT.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_Tab3DdownGMT.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3DdownGMT.add_event_cb(self.emngr.changeGMT_evt_hndlr, lv.EVENT.ALL, None)

        self.ui_Tab3lblWIFI = lv.label(self.tab3)
        self.ui_Tab3lblWIFI.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblWIFI.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblWIFI.set_pos(0, 215)
        self.ui_Tab3lblWIFI.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblWIFI.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_Tab3lblWIFI.set_style_text_font(lv.font_montserrat_22, 0)
        self.ui_Tab3lblWIFI.set_text("WiFi")

        self.ui_Tab3TextAreaSSID = lv.textarea(self.tab3)
        self.ui_Tab3TextAreaSSID.set_width(218)
        self.ui_Tab3TextAreaSSID.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3TextAreaSSID.set_pos(0, 243)
        self.ui_Tab3TextAreaSSID.set_text("SSID")
        self.ui_Tab3TextAreaSSID.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3TextAreaSSID.set_style_text_font(lv.font_montserrat_20, 0)

        self.ui_Tab3TextAreaWifiKEY = lv.textarea(self.tab3)
        self.ui_Tab3TextAreaWifiKEY.set_width(218)
        self.ui_Tab3TextAreaWifiKEY.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3TextAreaWifiKEY.set_pos(235, 243)
        self.ui_Tab3TextAreaWifiKEY.set_text("WIFI KEY")
        self.ui_Tab3TextAreaWifiKEY.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3TextAreaWifiKEY.set_style_text_font(lv.font_montserrat_20, 0)

        self.ui_Tab3lblSENSORS = lv.label(self.tab3)
        self.ui_Tab3lblSENSORS.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblSENSORS.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblSENSORS.set_pos(0, 300)
        self.ui_Tab3lblSENSORS.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblSENSORS.clear_flag(
            lv.obj.FLAG.PRESS_LOCK | lv.obj.FLAG.CLICK_FOCUSABLE
        )
        self.ui_Tab3lblSENSORS.set_style_text_font(lv.font_montserrat_22, 0)
        self.ui_Tab3lblSENSORS.set_text("Sensors")

        self.ui_Tab3DdownSENSORS = lv.dropdown(self.tab3)
        self.ui_Tab3DdownSENSORS.set_options(
            "\n".join(
                [
                    "Sensor 1",
                    "Sensor 2",
                    "Sensor 3",
                    "Sensor 4",
                    "Sensor 5",
                    "Sensor 6",
                    "Sensor 7",
                    "Sensor 8",
                ]
            )
        )
        self.ui_Tab3DdownSENSORS.set_width(104)
        self.ui_Tab3DdownSENSORS.set_height(40)
        self.ui_Tab3DdownSENSORS.set_pos(0, 330)
        self.ui_Tab3DdownSENSORS.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_Tab3DdownSENSORS.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

        self.ui_Tab3TxtArSensrorName = lv.textarea(self.tab3)
        self.ui_Tab3TxtArSensrorName.set_width(168)
        self.ui_Tab3TxtArSensrorName.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3TxtArSensrorName.set_pos(114, 330)
        self.ui_Tab3TxtArSensrorName.set_text("Sensor Name")
        self.ui_Tab3TxtArSensrorName.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3TxtArSensrorName.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_Tab3TxtArSensrorIP = lv.textarea(self.tab3)
        self.ui_Tab3TxtArSensrorIP.set_width(168)
        self.ui_Tab3TxtArSensrorIP.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3TxtArSensrorIP.set_pos(292, 330)
        self.ui_Tab3TxtArSensrorIP.set_text("Sensor IP")
        self.ui_Tab3TxtArSensrorIP.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3TxtArSensrorIP.set_style_text_font(lv.font_montserrat_14, 0)

        self.ui_Tab3BtnReboot = lv.btn(self.tab3)
        self.ui_Tab3BtnReboot.set_width(80)
        self.ui_Tab3BtnReboot.set_height(40)
        self.ui_Tab3BtnReboot.set_pos(175, 385)
        self.ui_Tab3BtnReboot.add_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        self.ui_Tab3BtnReboot.clear_flag(lv.obj.FLAG.SCROLLABLE)
        self.ui_Tab3BtnReboot.set_style_text_color(
            lv.color_hex(0x808080), lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab3BtnReboot.set_style_text_opa(255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.ui_Tab3BtnReboot.set_style_text_align(
            lv.TEXT_ALIGN.CENTER, lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab3BtnReboot.set_style_text_font(
            lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT
        )
        self.ui_Tab3BtnReboot.set_style_radius(lv.RADIUS_CIRCLE, 0)

        self.ui_Tab3lblbtnReboot = lv.label(self.ui_Tab3BtnReboot)
        self.ui_Tab3lblbtnReboot.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblbtnReboot.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblbtnReboot.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_Tab3lblbtnReboot.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblbtnReboot.set_style_text_font(lv.font_montserrat_28, 0)
        self.ui_Tab3lblbtnReboot.set_text(lv.SYMBOL.REFRESH)

        ##################### END TAB SETTINGS ################

        ############### FLOATTING BUTTONS ############

        self.ui_Tab3ButtonApply = lv.btn(self.tab3)
        self.ui_Tab3ButtonApply.set_width(158)
        self.ui_Tab3ButtonApply.set_height(35)
        self.ui_Tab3ButtonApply.align(lv.ALIGN.BOTTOM_LEFT, 0, 0)
        self.ui_Tab3ButtonApply.add_flag(lv.obj.FLAG.FLOATING | lv.obj.FLAG.CLICKABLE)
        self.ui_Tab3lblApply = lv.label(self.ui_Tab3ButtonApply)
        self.ui_Tab3lblApply.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblApply.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblApply.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_Tab3lblApply.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblApply.set_style_text_font(lv.font_montserrat_18, 0)
        self.ui_Tab3lblApply.set_text("APPLY")

        self.ui_Tab3ButtonCancel = lv.btn(self.tab3)
        self.ui_Tab3ButtonCancel.set_width(158)
        self.ui_Tab3ButtonCancel.set_height(35)
        self.ui_Tab3ButtonCancel.align(lv.ALIGN.BOTTOM_RIGHT, 0, 0)
        self.ui_Tab3ButtonCancel.add_flag(lv.obj.FLAG.FLOATING | lv.obj.FLAG.CLICKABLE)
        self.ui_Tab3lblCancel = lv.label(self.ui_Tab3ButtonCancel)
        self.ui_Tab3lblCancel.set_width(lv.SIZE_CONTENT)
        self.ui_Tab3lblCancel.set_height(lv.SIZE_CONTENT)
        self.ui_Tab3lblCancel.align(lv.ALIGN.CENTER, 0, 0)
        self.ui_Tab3lblCancel.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        self.ui_Tab3lblCancel.set_style_text_font(lv.font_montserrat_18, 0)
        self.ui_Tab3lblCancel.set_text("CANCEL")


################################################
