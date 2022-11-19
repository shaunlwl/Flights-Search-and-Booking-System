import datetime as dt

def LoadInitialData(airlines_list, aircraft_type_list, scheduled_flights):
  
  #Load Airlines
  SQ = airlines("Singapore Airlines","SQ")
  QF = airlines("Qantas", "QF")
  airlines_list.append(SQ)
  airlines_list.append(QF)

  #Load Aircraft Type
  aircraft_type_list.append(aircraft_type("Boeing 747", ["F", "J", "Y"], {"F":"1-1-1","J":"2-2-2","Y":"3-4-3"}, {"F":[1,10],"J":[11,20],"Y":[21,50]}))
  SQ.setAircraftType(aircraft_type_list[0])
  QF.setAircraftType(aircraft_type_list[0])

  #Load Flights
  scheduled_flights.append(flights("SQ", "123","SIN", "NRT", dt.datetime.strptime("5 Dec 22, 10:00AM", '%d %b %y, %I:%M%p'), 6.5, 3, "Boeing 747", {"F": 2000, "J": 1000, "Y":500}, "321"))
  scheduled_flights.append(flights("SQ", "456","SYD", "SIN", dt.datetime.strptime("4 Dec 22, 10:00PM", '%d %b %y, %I:%M%p'), 8, 2, "Boeing 747", {"F": 1500, "J": 750, "Y":300}, "654"))
  scheduled_flights.append(flights("SQ", "789","SYD", "NRT", dt.datetime.strptime("5 Dec 22, 09:00AM", '%d %b %y, %I:%M%p'), 14, 2, "Boeing 747", {"F": 3500, "J": 2500, "Y":1500}, "987"))
  scheduled_flights.append(flights("QF", "789","SYD", "NRT", dt.datetime.strptime("5 Dec 22, 01:00PM", '%d %b %y, %I:%M%p'), 14.5, 2, "Boeing 747", {"F": 3200, "J": 2200, "Y":1200}, "987"))
  scheduled_flights.append(flights("SQ", "123","SIN", "NRT", dt.datetime.strptime("12 Dec 22, 10:00AM", '%d %b %y, %I:%M%p'), 6.5, 3, "Boeing 747", {"F": 2000, "J": 1000, "Y":500}, "321"))
  scheduled_flights.append(flights("SQ", "456","SYD", "SIN", dt.datetime.strptime("11 Dec 22, 10:00PM", '%d %b %y, %I:%M%p'), 8, 2, "Boeing 747", {"F": 1500, "J": 750, "Y":300}, "654"))
  scheduled_flights.append(flights("SQ", "789","SYD", "NRT", dt.datetime.strptime("12 Dec 22, 09:00AM", '%d %b %y, %I:%M%p'), 14, 2, "Boeing 747", {"F": 3500, "J": 2500, "Y":1500}, "987"))
  scheduled_flights.append(flights("QF", "789","SYD", "NRT", dt.datetime.strptime("12 Dec 22, 01:00PM", '%d %b %y, %I:%M%p'), 14.5, 2, "Boeing 747", {"F": 3200, "J": 2200, "Y":1200}, "987"))
  
  return airlines_list, aircraft_type_list, scheduled_flights 



def createAirline(name, IATA_code, airlines_list):
  airlines_list.append(airlines(name, IATA_code))



#Airlines Class

class airlines:
  def __init__(self, name, IATA_code):
    self._name = name
    self._IATA = IATA_code
    self._aircraft_type = []

  def getName(self):
    return self._name

  def setName(self, name):
    self._name = name
    

  def getIATA(self):
    return self._IATA

  def setIATA(self, IATA_code):
    self._IATA = IATA_code
  
  def getAircraftType(self):
    return self._aircraft_type

  def setAircraftType(self, aircraft_type):
    self._aircraft_type.append(aircraft_type)
    



#Aircraft Type Class

class aircraft_type:
  def __init__(self, name, cabin_class, seat_config, seat_start_end):
    self._name = name
    self._cabin_class = cabin_class
    self._seat_config = seat_config
    self._cabin_start_end_rows = seat_start_end
    self._seats_layout = {}
    
    if len(list(seat_config.keys())) != len(list(seat_start_end.keys())):
      
      print("\nERROR: Seat Configuration and Start and End Rows per Cabin Class have errorneous information\n")
    
    else:

      for i in range(0,len(list(seat_config.keys()))): #Choose the cabin class
        
        
        seat_arrangement = seat_config[list(seat_config.keys())[i]].split("-")    #[1,1,1]
        row_number = seat_start_end[list(seat_start_end.keys())[i]][0]
        
        while row_number <= seat_start_end[list(seat_start_end.keys())[i]][1]:
          start_char = "A"
                    
          for items in seat_arrangement:
            items = int(items)
            j = 1

            while j <= items: 
              
              if list(seat_config.keys())[i] not in self._seats_layout.keys():
                self._seats_layout[list(seat_config.keys())[i]] = [str(row_number)+start_char]
              else:
                self._seats_layout[list(seat_config.keys())[i]].append(str(row_number)+start_char)
              j += 1
              start_char = chr(ord(start_char) + 1)
          
          row_number += 1

      

        


  def getName(self):
    return self._name

  def setName(self, name):
    self._name = name
    
  def getCabinClass(self):
    return self._cabin_class

  def setCabinClass(self, cabin_class):
    self._cabin_class = cabin_class

  def getSeatConfig(self):
    return self._seat_config

  def setSeatConfig(self, seat_config):
    self._seat_config = seat_config
  
  def getCabinStartandEnd(self):
    return self._cabin_start_end_rows

  def setCabinStartandEnd(self, seat_start_end):
    self._cabin_start_end_rows = seat_start_end

  def getSeatsLayout(self):
    return self._seats_layout



#Flights Class

class flights:
  def __init__(self, IATA_code, out_flight_no,  origin_airport, destination_airport, dept_date_time, flight_hours, stopover_dur, aircarft_type, fare_amount, in_flight_no = None):
    self._IATA = IATA_code
    self._outbound = out_flight_no
    self._inbound = in_flight_no
    self._origin = origin_airport
    self._dest = destination_airport
    self._dept_datetime = dept_date_time
    self._flight_hours = flight_hours
    self._stopover_dur = stopover_dur
    self._fare_armount = fare_amount
    self._aircraft_type = aircarft_type
    
  
  def getIATA(self):
    return self._IATA

  def setIATA(self, IATA_code):
    self._IATA = IATA_code
    

  def getOutbound(self): #Outbound Flight No.
    return self._outbound

  def setOutbound(self, out_flight_no):
    self._outbound = out_flight_no

  def getInbound(self): #Inbound Flight No.
    return self._inbound

  def setInbound(self, in_flight_no):
    self._inbound = in_flight_no
  
  def getAircraftType(self):
    return self._aircraft_type

  def setAircraftType(self, aircraft_type):
    self._aircraft_type = aircraft_type

  def getOrigin(self):
    return self._origin

  def setOrigin(self, origin_airport):
    self._origin = origin_airport
  
  def getDestination(self):
    return self._dest

  def setDestination(self, destination_airport):
    self._dest = destination_airport
  
  def getDepartureDateTime(self):
    return self._dept_datetime

  def setDepartureDatetime(self, dept_date_time):
    self._dept_datetime = dept_date_time
  
  def getFlightHours(self):
    return self._flight_hours

  def setFlightHours(self, flight_hours):
    self._flight_hours = flight_hours
  
  def getStopoverDuration(self):
    return self._stopover_dur

  def setStepoverDuration(self, stopover_dur):
    self._stopover_dur = stopover_dur
  
  def getFareAmount(self):
    return self._fare_armount

  def setFareAmount(self, fare_amount):
    self._fare_armount = fare_amount
  
  

