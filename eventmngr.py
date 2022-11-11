import lvgl as lv
import _thread
import time
try:
    import usocket as _socket
except:
    import _socket
try:
    import ussl as ssl
except:
    import ssl
import ujson
import errno


class eventmngr:
    def __init__(self):

        self.graphics = None
        self.EndState = False
        self.runningTask = None
        self.exitThread = False
        self.toOFF = False
        self.checkboxvalue = 0x00
        self.Automatic = 0x01
        self.All_Delayed = 0x02
        self.Zones_Time = 0x04
        self.All_To_Off = 0x08
        self.Zones_Time_Off = 0x10
        self.conf = None
        self.mappingTime = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
        ]
        self.statusRunningProgram = [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]
        self.currentProgram = None

    def setGraph(self, graph=None):  # set interface vars linked to local
        self.graphics = graph if graph else None

    def setconf(self, conf=None):  # set configs vars linked to local
        self.conf = conf if conf else None
        # print (self.conf.settings.programset)

    def commitConfToFile(self):
        self.conf.confWrite()

    ########### Task executors


    ###### Rutina que trabaja sobre un programa especifico y lo que tenga habilitado

    def programZones(
        self, delay, id, programSelected
    ):  # run preprogramed zone manually

        if (
            self.toOFF
        ):  # Write conf at top, in case of any trouble during delay, restart in the right condition
            self.graphics.ui_SwitchOnOff.clear_state(lv.STATE.CHECKED)
            self.conf.configdata["TabHome"]["OnOff"] = False
            self.commitConfToFile()
        time.sleep(delay * 60)  # Delayed Start in minutes
        self.runningTask = id  # debbuging purpose
        self.statusRunningProgram[programSelected] = True

        for i in range(8):
            running_time_zone = self.conf.settings.programset[programSelected][1][i]
            # print(f"Debug Program %d Zone %d Time %d" % (programSelected,i, running_time_zone))
            endtime = time.time() + (running_time_zone * 60)
            passcounter = 0
            while time.time() < endtime and not self.exitThread:
                passcounter = passcounter + 1
                if passcounter % 2:
                    self.graphics.lblobjtemp[i].add_flag(lv.obj.FLAG.HIDDEN)
                else:
                    self.graphics.lblobjtemp[i].clear_flag(lv.obj.FLAG.HIDDEN)
                print(f"DEBUG Activo Pin Regador %d" % i)  # Replace with action
                time.sleep(1)
            print(f"DEBUG Desactivo Pin Regador %d" % i)  # Replace with action
            if self.exitThread:
                break
            self.graphics.lblobjtemp[i].clear_flag(lv.obj.FLAG.HIDDEN)
        # TO-DO desactivar todos los regadores por si cae justo en el cambio de zona
        self.graphics.lblobjtemp[i].clear_flag(lv.obj.FLAG.HIDDEN)
        self.runningTask = None
        self.exitThread = False
        self.statusRunningProgram[programSelected] = False

        ###### Rutina que trabaja solo sobre zonas habilitadas

    def ManualZones(self, delay, id, checkboxenable):  # run preprogramed zone manually
        if (
            self.toOFF
        ):  # Write conf at top, in case of any trouble during delay, restart in the right condition
            self.graphics.ui_SwitchOnOff.clear_state(lv.STATE.CHECKED)
            self.conf.configdata["TabHome"]["OnOff"] = False
            self.commitConfToFile()
        self.checkboxenable = checkboxenable if checkboxenable else 0x0
        runtime = self.mappingTime[self.graphics.ui_RolManRunTime.get_selected()]
        time.sleep(delay * 60)  # Delayed Start in minutes
        self.runningTask = id  # debbuging purpose
        for i in range(8):
            if self.checkboxenable & (1 << i):
                # print(f"%d Enable" % (i+1)) #debug
                endtime = time.time() + (runtime * 60)
                passcounter = 0
                while time.time() < endtime and not self.exitThread:
                    passcounter = passcounter + 1
                    if passcounter % 2:
                        self.graphics.lblobjtemp[i].add_flag(lv.obj.FLAG.HIDDEN)
                    else:
                        self.graphics.lblobjtemp[i].clear_flag(lv.obj.FLAG.HIDDEN)
                    print(f"DEBUG Activo Pin Regador %d" % i)  # Replace with action
                    time.sleep(1)
                print(f"DEBUG Desactivo Pin Regador %d" % i)  # Replace with action
                if self.exitThread:
                    break
            # else:
            # 	print(f"%d Disable" % (i+1))  #Just for debug
            # 	continue
            self.graphics.lblobjtemp[i].clear_flag(lv.obj.FLAG.HIDDEN)

        self.graphics.lblobjtemp[i].clear_flag(lv.obj.FLAG.HIDDEN)
        self.exitThread = False
        self.runningTask = None
        # TO-DO desactivar todos los regadores por si cae un exit justo en el cambio de zona

    ######### END Task Executors

    ############# Separate Tasks Starters as Facades

    def runprogramZones(self, startdelay=None, programSelected=None):
        _thread.start_new_thread(
            self.programZones, (startdelay, self.All_Delayed, programSelected)
        )
        pass

    def runManualZones(self, startdelay=None, checkboxenable=None):
        _thread.start_new_thread(
            self.ManualZones, (startdelay, self.Zones_Time, checkboxenable)
        )
        pass

    def clockupdate(self,timerClock):
    	self.clockupdatelocal()

    ############# END Separate Tasks Starters as Facades


    def getLocation(self):
    	s = _socket.socket()
    	ai = _socket.getaddrinfo("ip-api.com", 80)
    	addr = ai[0][-1]


    	try:
    		s.connect(addr)
    	except Exception as err:
    		print (f"Caught exception socket.error : %s" % err)
    		return "Error","Error","Error"

    	s.write(b"GET /json/ HTTP/1.0\r\n\r\n")
        var=s.read(4096)
        s.close()
        var=var.decode()
        try:
        	jsonstring=str(var[var.find('{'):len(var)])     
        	#print(jsonstring)
        	location=ujson.loads(jsonstring)
        except (NameError, TypeError) as error:
			print(error)
			return "Error","Er","Error"
        status=location["status"]
        countryName= location["country"]
        countryCode=location["countryCode"]  #Se usa este
        countryRegion=location["region"]
        RegionName=location["regionName"]
        Querycity=location["city"]          #Con Este para consultar a openweather
        if status=="success":
        	return  countryName , countryCode , Querycity
        else:
        	return "Error","Er","Error"



    ######################### Start Handlers

    def getBoxesStatus(self):
        if self.graphics is not None:
            checkboxvalue = 0x00
            if self.graphics.ui_ChBoxZona1.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 1
            if self.graphics.ui_ChBoxZona2.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 2
            if self.graphics.ui_ChBoxZona3.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 4
            if self.graphics.ui_ChBoxZona4.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 8
            if self.graphics.ui_ChBoxZona5.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 16
            if self.graphics.ui_ChBoxZona6.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 32
            if self.graphics.ui_ChBoxZona7.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 64
            if self.graphics.ui_ChBoxZona8.get_state() & lv.STATE.CHECKED:
                checkboxvalue = checkboxvalue | 128
            return checkboxvalue

    def ui_DropdownMode_evt_hndlr(self, e):  # Tab1 DropDown Mode
        code = e.get_code()
        obj = e.get_target()
        if code == lv.EVENT.VALUE_CHANGED:

            if (
                obj.get_selected() == 0
                or obj.get_selected() == 1
                or obj.get_selected() == 3
            ):  # No manual Zones for this options
                self.graphics.ui_ChBoxZona1.add_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona2.add_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona3.add_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona4.add_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona5.add_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona6.add_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona7.add_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona8.add_state(lv.STATE.DISABLED)
            else:  # Manual Zones Enabled
                self.graphics.ui_ChBoxZona1.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona2.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona3.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona4.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona5.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona6.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona7.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_ChBoxZona8.clear_state(lv.STATE.DISABLED)

            if obj.get_selected() == 0:
                self.graphics.ui_RolManRunTime.set_options(
                    "\n".join(self.graphics.configuredtime), lv.roller.MODE.INFINITE
                )
                self.graphics.ui_RolManRunTime.add_state(lv.STATE.DISABLED)
                self.graphics.ui_RolManDelay.add_state(lv.STATE.DISABLED)
                self.graphics.ui_RolManRunTime.set_selected(0, lv.ANIM.OFF)
                self.graphics.ui_RolManDelay.set_selected(0, lv.ANIM.OFF)
                self.graphics.ui_LabelStatus.set_style_text_font(
                    lv.font_montserrat_20, 0
                )
                self.EndState = True  # Cuando termina, puede empezar automatico
            else:
                self.graphics.ui_RolManRunTime.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_RolManRunTime.set_selected(0, lv.ANIM.OFF)
                self.graphics.ui_RolManDelay.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_RolManDelay.set_selected(0, lv.ANIM.OFF)

                ####Poner Logica

            if obj.get_selected() == 1 or obj.get_selected() == 3:
                self.graphics.ui_RolManRunTime.set_options(
                    "\n".join(self.graphics.configuredtime_program),
                    lv.roller.MODE.INFINITE,
                )
                self.graphics.ui_LabelStatus.set_style_text_font(
                    lv.font_montserrat_16, 0
                )
                if obj.get_selected() == 1:
                    self.EndState = True  # Cuando termina, puede empezar automatico
                else:
                    self.EndState = False
                ####Poner Logica

            if obj.get_selected() == 2 or obj.get_selected() == 4:
                self.graphics.ui_RolManRunTime.set_options(
                    "\n".join(self.graphics.configuredtime_manual),
                    lv.roller.MODE.INFINITE,
                )
                self.graphics.ui_LabelStatus.set_style_text_font(
                    lv.font_montserrat_16, 0
                )
                if obj.get_selected() == 2:
                    self.EndState = True  # Cuando termina, puede empezar automatico
                else:
                    self.EndState = (
                        False  ##Cuando termina, no debe volver empezar automatico
                    )
                    self.graphics.ui_LabelStatus.set_style_text_font(
                        lv.font_montserrat_14, 0
                    )

            if obj.get_selected() > 4 or obj.get_selected() < 0:
                print("Error en seleccion")

            option = " " * 20
            obj.get_selected_str(option, len(option))
            self.graphics.ui_LabelStatus.set_text(option.strip())

    def ui_RUN_evt_hndlr(self, e):  # Tab1 Play Button
        code = e.get_code()
        self.getBoxesStatus()
        if code == lv.EVENT.CLICKED:
            if self.runningTask is not None:
                self.exitThread = True
                pass

            if self.graphics.ui_DropdownMode.get_selected() == 0:  # "Automatic"
                pass

            if self.graphics.ui_DropdownMode.get_selected() == 1:  # "Pgrm Delayed"
                self.toOFF = False
                programSelected = self.graphics.ui_RolManRunTime.get_selected()
                self.runprogramZones(
                    self.graphics.ui_RolManDelay.get_selected(), programSelected
                )

            if self.graphics.ui_DropdownMode.get_selected() == 2:  # "Zones & Time"
                self.toOFF = False
                self.runManualZones(
                    self.graphics.ui_RolManDelay.get_selected(), self.getBoxesStatus()
                )
                pass

            if self.graphics.ui_DropdownMode.get_selected() == 3:  # "Pgrm To Off"
                self.toOFF = True
                programSelected = self.graphics.ui_RolManRunTime.get_selected()
                self.runprogramZones(
                    self.graphics.ui_RolManDelay.get_selected(), programSelected
                )

            if self.graphics.ui_DropdownMode.get_selected() == 4:  # "Zones & Time Off"
                self.toOFF = True
                pass
        elif code == lv.EVENT.VALUE_CHANGED:
            # print("Value changed seen")
            pass

    """
	################ CONTROLES GENERALES ##################
	#Cuando cambio de programa, solo muestro el status configurado
		Leer dias, hora, minuto, poner zona0,runningtime para zona 0
	#Si cambio la hora, debo modificar la configuracion y guardarlo
	#Si cambio el minuto, debo modificar la configuracion y guardarlo
	#Si la zona solo muestro el status configurado
	#Si cambio el running time, debo modificar la configuracion y guardarlo
	#Si cambio los dias, debo modificar la configuracion y guardarlo
	"""

    def ui_Tab3RollerPgm_evt_hndlr(
        self, e
    ):  # Cuando cambio de programa, solo muestro el status configurado
        code = e.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            # print("Se modifico el evento Programa")
            self.currentProgram = self.graphics.ui_Tab3RollerPgm.get_selected()
            self.graphics.ui_Tab3RollerTimeH.set_selected(  # Seteo la hora
                self.conf.settings.programset[self.currentProgram][0][0], lv.ANIM.OFF
            )
            self.graphics.ui_Tab3RollerTimeM.set_selected(  # Seteo el Minuto
                self.conf.settings.programset[self.currentProgram][0][1], lv.ANIM.OFF
            )
            self.graphics.ui_Tab3RollerZone.set_selected(
                0, lv.ANIM.OFF
            )  # Seteo La primera zona
            self.graphics.ui_Tab3RollRunningTime.set_selected(
                self.conf.settings.programset[self.currentProgram][1][0], lv.ANIM.OFF
            )
            for i in range(7):
                if self.conf.settings.programset[self.currentProgram][2][i] > 0:
                    self.graphics.ui_ChBoxMatrix[i].add_state(lv.STATE.CHECKED)
                else:
                    self.graphics.ui_ChBoxMatrix[i].clear_state(lv.STATE.CHECKED)
            if self.graphics.ui_Tab3RollerTimeH.get_selected() == 24:
                self.graphics.ui_Tab3RollerTimeM.add_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollerZone.add_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollRunningTime.add_state(lv.STATE.DISABLED)
            else:
                self.graphics.ui_Tab3RollerTimeM.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollerZone.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollRunningTime.clear_state(lv.STATE.DISABLED)

    def ui_Tab3RollerTimeH_evt_hndlr(
        self, e
    ):  # Si cambio la hora, debo modificar la configuracion y guardarlo
        code = e.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            programatemp = "Program" + str(self.currentProgram)
            self.conf.configdata["TabSettings"]["Programs"][programatemp][
                "startHour"
            ] = self.conf.settings.programset[self.currentProgram][0][
                0
            ] = self.graphics.ui_Tab3RollerTimeH.get_selected()
            #####Llamar a escribir el json al archivo
            self.commitConfToFile()
            if self.graphics.ui_Tab3RollerTimeH.get_selected() == 24:
                self.graphics.ui_Tab3RollerTimeM.add_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollerZone.add_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollRunningTime.add_state(lv.STATE.DISABLED)
            else:
                self.graphics.ui_Tab3RollerTimeM.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollerZone.clear_state(lv.STATE.DISABLED)
                self.graphics.ui_Tab3RollRunningTime.clear_state(lv.STATE.DISABLED)

    def ui_Tab3RollerTimeM_evt_hndlr(
        self, e
    ):  # Si cambio el minuto, debo modificar la configuracion y guardarlo
        code = e.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            programatemp = "Program" + str(self.currentProgram)
            self.conf.configdata["TabSettings"]["Programs"][programatemp][
                "startMin"
            ] = self.conf.settings.programset[self.currentProgram][0][
                1
            ] = self.graphics.ui_Tab3RollerTimeM.get_selected()
            #####Llamar a escribir el json al archivo
            self.commitConfToFile()

    def ui_Tab3RollerZone_evt_hndlr(
        self, e
    ):  # Si cambio la zona solo muestro el status configurado
        code = e.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            self.graphics.ui_Tab3RollRunningTime.set_selected(
                self.conf.settings.programset[self.currentProgram][1][
                    self.graphics.ui_Tab3RollerZone.get_selected()
                ],
                lv.ANIM.OFF,
            )

    def ui_Tab3RollRunningTime_evt_hndlr(
        self, e
    ):  # Si cambio el running time, debo modificar la configuracion y guardarlo
        code = e.get_code()
        if code == lv.EVENT.VALUE_CHANGED:
            programatemp = "Program" + str(self.currentProgram)
            zonetemp = self.graphics.ui_Tab3RollerZone.get_selected()
            self.conf.configdata["TabSettings"]["Programs"][programatemp]["Zone"][
                str(zonetemp)
            ] = self.conf.settings.programset[self.currentProgram][1][
                zonetemp
            ] = self.graphics.ui_Tab3RollRunningTime.get_selected()
            #####Llamar a escribir el json al archivo
            self.commitConfToFile()

    def ui_ChBoxMatrix_evt_hndlr(
        self, e
    ):  # Si cambio los dias, debo modificar la configuracion y guardarlo
        code = e.get_code()
        programatemp = "Program" + str(self.currentProgram)
        if code == lv.EVENT.CLICKED:
            for i in range(7):
                self.conf.settings.programset[self.currentProgram][2][i] = (
                    self.graphics.ui_ChBoxMatrix[i].get_state() & lv.STATE.CHECKED
                )
                if self.conf.settings.programset[self.currentProgram][2][i] == 1:
                    self.conf.configdata["TabSettings"]["Programs"][programatemp][
                        "RunningDays"
                    ][str(i)] = True
                else:
                    self.conf.configdata["TabSettings"]["Programs"][programatemp][
                        "RunningDays"
                    ][str(i)] = False
            #####Llamar a escribir el json al archivo
            self.commitConfToFile()

    def CheckPrograms(self):
        GMTTEST = self.conf.settings.GMT
        horatocheck = time.time() + (GMTTEST * 3600)
        horacheck = time.gmtime(horatocheck)[3]
        minutocheck = time.gmtime(horatocheck)[4]
        daytocheck = time.gmtime(horatocheck)[6]
        for i in range(16):
            if self.statusRunningProgram[
                i
            ]:  # If the selected program is runnning, ignore and continue
                continue
            if self.conf.settings.programset[i][2][daytocheck]:
                if self.conf.settings.programset[i][0][0] == horacheck:
                    if self.conf.settings.programset[i][0][1] == minutocheck:
                        print(f"Me toca regar el programa %d" % i)
                        self.runprogramZones(startdelay=0, programSelected=i)

    def getGeoLocatio_evt_hndlr(self, e):
    	code = e.get_code()
        if code == lv.EVENT.CLICKED:
        	Country,Ccode,City=self.getLocation()
        	self.graphics.ui_Tab3lblCountry.set_text(Country+", "+Ccode)
        	self.graphics.ui_Tab3lblCity.set_text(City)
	        if Country != "Error" and Ccode !="Er" and City !="Error":
	        	self.conf.settings.Country = Country
	        	self.conf.configdata["TabSettings"]["ForeCast"]["Country"]=Country
	        	self.conf.settings.City = City
	        	self.conf.configdata["TabSettings"]["ForeCast"]["City"]=City
	        	self.conf.settings.CountryCode=Ccode
	        	self.conf.configdata["TabSettings"]["ForeCast"]["CountryCode"]=Ccode
	        	self.commitConfToFile()


    def clockupdatelocal(self):
        global horaactual
        horaactual = time.time()+(self.conf.settings.GMT*3600)
        horalocal = "{0:02d}:{1:02d}".format(time.gmtime(horaactual)[3],time.gmtime(horaactual)[4])
        self.graphics.ui_Label1HoraActual.set_text(horalocal)

    def changeGMT_evt_hndlr(self, e):
    	global GMTValue
    	code = e.get_code()
    	if code == lv.EVENT.VALUE_CHANGED:
    		option = " "*4
    		self.graphics.ui_Tab3DdownGMT.get_selected_str(option,len(option))
    		option=option.strip()
    		option=int(option[0:len(option)-1])
    		self.conf.settings.GMT = self.conf.configdata["TabSettings"]["ForeCast"]["GMT"]=option
    		GMTValue=option
    		self.commitConfToFile()
    		self.clockupdatelocal()




    		



################ END HANDLERS

    	
