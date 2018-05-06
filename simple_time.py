
class SimpleTime():

    def __init__(self, day = 0, hour = 0, minute = 0):
        self.day = day
        self.hour = hour
        self.minute = minute

    def byte_to_time(self, first = 0, second = 0):
        self.day = ((first & 0xF8) >> 3)
        self.hour = (((first & 0x07) << 2) + ((second & 0xC0) >> 6))
        self.minute = (second & 0x3F)

    def print_time(self):
        print("Day: \t", self.day)
        print("Hour: \t", self.hour)
        print("Min: \t", self.minute)
