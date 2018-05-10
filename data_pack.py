from simple_time import SimpleTime

class DataPack():
    def __init__(self):
        self.reset()

    def reset(self):
        self.station_id = None
        self.time = SimpleTime()

        self.has_bat_lvl = False
        self.has_air_temp = False
        self.has_air_hum = False
        self.has_air_pres = False

        self.bat_lvl = None
        self.air_temp = None
        self.air_hum = None
        self.air_pres = None

        self.dict = None
    
    def buildDict(self):
        self.dict = dict()
        if self.has_bat_lvl:
            self.dict["batteryLevel"] = self.bat_lvl
        if self.has_air_temp:
            self.dict["airTemperatur"] = self.air_temp
        if self.has_air_hum:
            self.dict["airHumidity"] = self.air_hum
        if self.has_air_pres:
            self.dict["airPressure"] = self.air_pres