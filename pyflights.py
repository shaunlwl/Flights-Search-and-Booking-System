import datetime as dt
import class_functions as cf



def main():
    airlines_list = []
    aircraft_type_list = []
    scheduled_flights = []
    
    airlines_list, aircraft_type_list, scheduled_flights = cf.LoadInitialData(airlines_list, aircraft_type_list, scheduled_flights)
    
    while True:

        user_input = input("Please choose from the following list of options:\n1: Create Airline\n2: Create Aircraft Type\n3: Create Flight\n4: Search and Book Flight\n")
        

        if user_input not in ["1", "2", "3", "4"]:
            
            print("\nERROR: You have entered an inalid input, Please try again\n")
            continue

        else:

            if user_input == "1": #Create Airline
                
                user_input = input("\nPlease enter Airline Name followed by IATA Code, separated by commas as such: Singapore Airlines, SQ\n").strip().split(",")
                
                if len(user_input) != 2:
                    print("\nERROR: You have entered an invalid amount of inputs, Please try again")
               
                else:

                    airline_already_exist = False
                    name = user_input[0].strip()
                    IATA_code = user_input[1].strip()
                    for items in airlines_list:
                        if IATA_code.lower() == items.getIATA().lower():
                            print("\nERROR: Airline already exists in the system\n")
                            airline_already_exist = True
                            break
                    
                    if airline_already_exist == False:
                        cf.createAirline(name.capitalize(), IATA_code.upper(), airlines_list)
                        print("\n Airline created successfully!\n")


        
            if user_input == "2": #Create Aircraft Type
                
                user_input = input("\nPlease input Airline IATA Code followed by Aircraft Type Name separated by commas as such: SQ, Boeing 747\n").strip().split(",")

                if len(user_input) != 2:
                    print("\nERROR: You have entered an invalid amount of inputs, Please try again")
                
                else:
                    airlines_exist = False
                    aircraft_type_exist = False

                    IATA_code = user_input[0].strip()
                    type_name = user_input[1].strip()

                    for items in airlines_list:
                        if IATA_code.lower() == items.getIATA().lower():
                            airlines_exist = True
                            break
                    
                    for items in aircraft_type_list:
                        if type_name.lower() == items.getName().lower():
                            aircraft_type_exist = True
                            break
                    
                    if airlines_exist == True and aircraft_type_exist == False: #Only Case when Aircraft Type should be created
                        
                        cabin_class = []
                        seat_config = {}
                        seat_start_end = {}

                        while True:

                            user_input = input("Do you want to add Cabin Class? Y/N\n").lower()
                            if user_input not in ["y", "n"]:
                                print("\nERROR: You have entered an invalid input, Please try again\n")
                                continue
                            else:
                                
                                if user_input == "n":
                                    
                                    break
                                
                                else:
                                    cabin_details = input("\nPlease enter Cabin Class details in this format:\nCabin Class , Seat Configuration, Starting Row Number, Ending Row Number(inclusive)\nY, 1-1-1 , 1 , 10\n").strip().split(",")
                                    
                                    if len(cabin_details) != 4:
                                        print("\nERROR: You have entered an invalid amount of inputs, Please try again")
                                        continue
                                    else:
                                        for i in range(0,len(cabin_details)):
                                            cabin_details[i] = cabin_details[i].strip()
                                        
                                        if cabin_details[0].lower() not in ["y", "f", "j", "w"]:
                                            print("\nERROR: You have entered an invalid Cabin Class, Please try again\n")
                                            continue

                                        if len(cabin_details[1].split("-")) <= 1 or len(cabin_details[1].split("-")) > 3:
                                            print("\nERROR: You have entered an invalid Seat Configuration, Please try again\n")
                                            continue
                                        
                                        if len(cabin_details[1].split("-")) == 3 or len(cabin_details[1].split("-")) == 2:
                                            cabin_seat_split = cabin_details[1].split("-")
                                            try:
                                                for i in range(0,len(cabin_seat_split)):
                                                    cabin_seat_split[i] = int(cabin_seat_split[i])
                                            
                                            except ValueError:
                                                print("\nERROR: You have entered an invalid input for Seat Configuration, a numeric value split by - is expected\n")
                                                continue

                                        try:

                                            cabin_details[2] = int(cabin_details[2])
                                            cabin_details[3] = int(cabin_details[3])
                                        
                                        except ValueError:
                                            print("\nERROR: You have entered an invalid input for either Starting Row Number OR Ending Row Number OR Both, a numeric value is expected\n")
                                            continue

                                        else:
                                            if cabin_details[0].upper() not in cabin_class:
                                                cabin_class.append(cabin_details[0].upper())
                                                seat_config[cabin_details[0].upper()] = cabin_details[1]
                                                seat_start_end[cabin_details[0].upper()] = [ cabin_details[2] , cabin_details[3]]
                                                continue
                                            else:
                                                print("\nERROR: Cabin Class {} has already been added previously".format(cabin_details[0].upper()))
                                                continue
                                
                        
                        if len(cabin_class) == 0:
                            
                            print("\nERROR: Aircraft Type cannot be created without a Cabin Class, Please try again\n")
                            
                        else:
                            
                            aircraft_type_list.append(cf.aircraft_type(type_name.capitalize(), cabin_class, seat_config, seat_start_end))

                            for items in airlines_list:
                                if IATA_code.lower() == items.getIATA().lower():
                                    items.setAircraftType(aircraft_type_list[-1])
                                    break

                            #Printing Output
                            print("\nAircraft Type {} created for {}".format(type_name.capitalize(), IATA_code.upper()))
                            
                            no_of_seats_per_cabin = 0
                            for items in cabin_class:
                                no_of_seats_per_row_list = seat_config[items].strip().split("-")
                                for i in range(0,len(no_of_seats_per_row_list)):
                                    no_of_seats_per_row_list[i] = int(no_of_seats_per_row_list[i])
                                no_of_seats_per_row = sum(no_of_seats_per_row_list)
                                start_char = "A"
                                end_char = chr(ord(start_char) + no_of_seats_per_row - 1)
                                start_row = seat_start_end[items][0]
                                end_row = seat_start_end[items][1]
                                print("Cabin Class {} - Seat {}{} to {}{} through {}{} to {}{}, {} seats".format(items.upper(),start_row,start_char,start_row,end_char, end_row, start_char, end_row, end_char,  len(aircraft_type_list[-1].getSeatsLayout()[items])))
                                no_of_seats_per_cabin = no_of_seats_per_cabin + len(aircraft_type_list[-1].getSeatsLayout()[items])
                                                        
                            print("Total {} seats".format(no_of_seats_per_cabin))

                    elif airlines_exist == False and aircraft_type_exist == False:
                        print("\nERROR: Given Airline does not exist in the system\n")

                    elif airlines_exist == False and aircraft_type_exist == True:
                        print("\nERROR: Given Airline does not exist in the system and Aircraft Type already exists in the system\n")

                    elif airlines_exist == True and aircraft_type_exist == True:
                        print("\nERROR: Aircraft Type already exists in the system\n")



            if user_input == "3": #Create Flight
                
                user_input = input("\nPlease input following details separated by commas:\n1. Airline IATA Code\n2. Outbound Flight Number\n3. Return Flight Number(Optional)\n4. Origin Airport IATA Code\n5. Destination Airport IATA code\n6. Departure Date/Time eg. 5 Dec 22, 10:00 AM\n7. Flight Time eg. 6 hour 30 minute\n8. Stopover Duration eg. 3 hour\n9. Aircraft Type\n").strip().split(",")

                if len(user_input) == 10: #Includes Return Flight Number
                    data_validated = cf.inputValidationforCreateFlight(user_input, airlines_list, aircraft_type_list, scheduled_flights)

                    if data_validated == True:
                        #Get Fare Amount input once data validation are done
                        user_input_fare = input("\nPlease Input Fare Amount by Cabin Class separated by commas. Eg. Cabin Class F - $2000, Cabin Class J - $1000, Cabin Class Y - $500\n").strip().split(",")
                        
                        if len(user_input_fare) > 4:
                            
                            print("\nERROR: There should only be four or fewer Cabin Classes, Please try again\n")

                        else:
                            fare_amount = {}
                            fare_error = False
                            for i in range(0, len(user_input_fare)):
                                temp = user_input_fare[i].strip().split("-")
                                
                                for j in range(0, len(temp)):
                                    temp[j] = temp[j].strip()

                                try:
                                    repetition_error = False
                                    if temp[0][-1] in list(fare_amount.keys()):
                                        print("ERROR: Repetition of Cabin Class detected, Please try again\n")
                                        repetition_error = True
                                        raise ValueError

                                    else:
                                        fare_amount[temp[0][-1]] = int(temp[1][1:])
                                
                                except ValueError:
                                    fare_error = True
                                    if repetition_error == True:
                                        pass
                                    else:
                                        print("\nERROR: Fare amount not in required format, Please try again\n")
                                
                                else:
                                    continue
                            
                            if fare_error == False:
                                flight_hours = user_input[7].strip().split(" ")
                                stopover_hours = user_input[8].strip().split(" ")

                                for i in range(0,len(flight_hours)):
                                    flight_hours[i] = flight_hours[i].strip()
            
                                for i in range(0,len(stopover_hours)):
                                    stopover_hours[i] = stopover_hours[i].strip()

            
                                flight_time = int(flight_hours[0]) + float(int(flight_hours[2])/60)
                                stopover_time = float(stopover_hours[0])
                                
                                for items in aircraft_type_list:
                                    if items.getName().lower() == user_input[9].lower():
                                        aircraft = items
                                        break
                                

                                scheduled_flights.append(cf.flights(user_input[0].upper(), int(user_input[1]),  user_input[3].upper(), user_input[4].upper(), user_input[5] , flight_time, stopover_time, aircraft, fare_amount, in_flight_no = int(user_input[2])))
                                print("\nFlight successfully added to system!\n")

                elif len(user_input) == 9: #Excludes Return Flight Number
                    
                    data_validated = cf.inputValidationforCreateFlight(user_input, airlines_list, aircraft_type_list, scheduled_flights)
                    
                    if data_validated == True:
                    
                        #Get Fare Amount input once data validation are done
                        user_input_fare = input("\nPlease Input Fare Amount by Cabin Class separated by commas. Eg. Cabin Class F - $2000, Cabin Class J - $1000, Cabin Class Y - $500\n").strip().split(",")

                        if len(user_input_fare) > 4:
                            
                            print("\nERROR: There should only be four or fewer Cabin Classes, Please try again\n")

                        else:
                            fare_amount = {}
                            fare_error = False
                            for i in range(0, len(user_input_fare)):
                                temp = user_input_fare[i].strip().split("-")
                                
                                for j in range(0, len(temp)):
                                    temp[j] = temp[j].strip()

                                try:
                                    repetition_error = False
                                    if temp[0][-1] in list(fare_amount.keys()):
                                        print("ERROR: Repetition of Cabin Class detected, Please try again\n")
                                        repetition_error = True
                                        raise ValueError

                                    else:
                                        fare_amount[temp[0][-1]] = int(temp[1][1:])
                                
                                except ValueError:
                                    fare_error = True
                                    if repetition_error == True:
                                        pass
                                    else:
                                        print("\nERROR: Fare amount not in required format, Please try again\n")
                                
                                else:
                                    continue
                            
                            if fare_error == False:
                                flight_hours = user_input[6].strip().split(" ")
                                stopover_hours = user_input[7].strip().split(" ")

                                for i in range(0,len(flight_hours)):
                                    flight_hours[i] = flight_hours[i].strip()
            
                                for i in range(0,len(stopover_hours)):
                                    stopover_hours[i] = stopover_hours[i].strip()

            
                                flight_time = int(flight_hours[0]) + float(int(flight_hours[2])/60)
                                stopover_time = float(stopover_hours[0])
                                
                                for items in aircraft_type_list:
                                    if items.getName().lower() == user_input[8].lower():
                                        aircraft = items
                                        break
                                
                                scheduled_flights.append(cf.flights(user_input[0].upper(), int(user_input[1]),  user_input[2].upper(), user_input[3].upper(), user_input[4] , flight_time, stopover_time, aircraft, fare_amount))
                                print("\nFlight successfully added to system!\n")

                else:                       
                    print("\nERROR: You have entered an invalid amount of inputs, Please try again")





            if user_input == "4": #Search and Book Flight
                
                user_input = input("\nPlease provide Trip Details separated by commas:\n1. Trip Type (Return or One-Way)\n2. Origin IATA Code\n3. Destination IATA Code\n4. Departure Date (eg. 5 Dec 22)\n5. Cabin Class (F or J or W or Y or No Preference)\n6. No. of Passenger(s)\n").strip().split(",")

                for i in range(0,len(user_input)):
                    user_input[i] = user_input[i].strip()

                if len(user_input) != 6:

                    print("\nERROR: You have entered an invalid amount of inputs, Please try again\n")

                else:
                    if user_input[0].lower() not in ["return", "one-way"]:
                        print("\nERROR: You have entered an invalid input for Trip Type, Please try again\n")
                    
                    else:
                        if user_input[4].lower() not in ["f", "j", "w", "y", "no preference"]:

                            print("\nERROR: You have entered an invalid input for Cabin Class, Please try again\n")
                        
                        else:

                            try:
                                user_input[3] = dt.datetime.strptime(user_input[3], '%d %b %y')
                                user_input[5] = int(user_input[5])
                                no_of_passengers = user_input[5]
                            
                            except ValueError:
                                print("\nERROR: You have entered an invalid input for either Departure Date or No. of Passenger(s), Please try again\n")
                        
                            else:
                                one_day_before = user_input[3] - dt.timedelta(days=1)
                                one_day_after = user_input[3] + dt.timedelta(days=1)
                                list_of_matching_direct_flights = []
                                pair_of_flights = [] #To hold those flights that are connected through a stopover

                                #Find matching Direct Flights
                                for flights in scheduled_flights:
                                    if flights.getDepartureDateTime().date() == user_input[3].date() or flights.getDepartureDateTime().date() == one_day_before.date() or flights.getDepartureDateTime().date() == one_day_after.date():
                                        if flights.getOrigin().upper() == user_input[1].upper() and flights.getDestination().upper() == user_input[2].upper():
                                            list_of_matching_direct_flights.append(flights)
                                

                                #Find matching stopover flights
                                stopover_screening_dict_origin = {}
                                for flights in scheduled_flights:
                                    if flights.getDepartureDateTime().date() == user_input[3].date() or flights.getDepartureDateTime().date() == one_day_before.date() or flights.getDepartureDateTime().date() == one_day_after.date():
                                        if flights.getOrigin().upper() == user_input[1].upper():
                                            if flights.getIATA().upper() not in [stopover_screening_dict_origin.keys()]:
                                                stopover_screening_dict_origin[flights.getIATA().upper()] = [flights]
                                            else:
                                                stopover_screening_dict_origin[flights.getIATA().upper()].append(flights)

                                stopover_screening_dict_dest = {}
                                for flights in scheduled_flights:
                                    if flights.getDepartureDateTime().date() == user_input[3].date() or flights.getDepartureDateTime().date() == one_day_before.date() or flights.getDepartureDateTime().date() == one_day_after.date():
                                        if flights.getOrigin().upper() == user_input[1].upper():
                                            if flights.getIATA().upper() not in [stopover_screening_dict_dest.keys()]:
                                                stopover_screening_dict_dest[flights.getIATA().upper()] = [flights]
                                            else:
                                                stopover_screening_dict_dest[flights.getIATA().upper()].append(flights)
                                
                                
                                for keys in list(stopover_screening_dict_origin.keys()):
                                    if keys not in list(stopover_screening_dict_dest.keys()):
                                        continue
                                    else:
                                        for items in stopover_screening_dict_origin[keys]:
                                            for connecting_flight in stopover_screening_dict_dest[keys]:
                                                if items.getDestination().upper() == connecting_flight.getOrigin().upper():
                                                    if items.getDepartureDateTime() + dt.timedelta(hours = items.getFlightHours()) < connecting_flight.getDepartureDateTime():
                                                        pair_of_flights.append([items, connecting_flight])

                                

                                #Print available flights
                                if len(list_of_matching_direct_flights) == 0 and len(pair_of_flights) == 0:
                                    print("\nNo flights available based on Trip details provided\n")
                                
                                else:
                                    result_count = 1 #To enumerate results
                                    no_seats_at_all = False
                                    no_seats_available_on_direct = False
                                    no_seats_available_on_connecting = False
                                    results_dict = {}
                                    if user_input[4].lower() == "no preference":
                                        
                                        if len(list_of_matching_direct_flights) != 0:
                                            for items in list_of_matching_direct_flights:
                                                for keys in list(items.getFareAmount().keys()):
                                                    if len(items.getSeatsAvailableonFlight()[keys]) >= user_input[5]:
                                                        print("Result {}:".format(result_count))
                                                        results_dict["result {}".format(result_count)] = [items, keys]
                                                        result_count +=1
                                                        departure_datetime = items.getDepartureDateTime()
                                                        arrival_datetime = items.getDepartureDateTime() + dt.timedelta(hours = items.getFlightHours())
                                                        print("{}{}, {} to {}, Depart {},\nArrive {}, Class {} Fare:${}".format(items.getIATA(), items.getOutbound(), items.getOrigin() , items.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'), keys ,items.getFareAmount()[keys]))
                                                        print("0 stopover, Total Fare ${}".format(user_input[5] * items.getFareAmount()[keys]))
                                                        print_count = 1
                                                        
                                                    
                                        if print_count != 1:
                                            no_seats_available_on_direct = True



                                        if len(pair_of_flights) != 0:
                                            flights_with_seats_on_connecting = []
                                            for items in pair_of_flights:
                                                count = 0
                                                for flights in items:
                                                    for keys in list(flights.getFareAmount().keys()):
                                                        if len(flights.getSeatsAvailableonFlight()[keys]) >= user_input[5]:
                                                            count += 1
                                                            break

                                                if count == 2:
                                                    flights_with_seats_on_connecting.append(items)

                                            if len(flights_with_seats_on_connecting) != 0:
                                                for items in flights_with_seats_on_connecting:                                                
                                                    
                                                    for flights in items:
                                                        for keys in list(flights.getFareAmount().keys()):
                                                            if len(flights.getSeatsAvailableonFlight()[keys]) >= user_input[5]:
                                                                print("Result {}:".format(result_count))
                                                                results_dict["result {}".format(result_count)] = [flights, keys]
                                                                result_count +=1
                                                                departure_datetime = flights.getDepartureDateTime()
                                                                arrival_datetime = flights.getDepartureDateTime() + dt.timedelta(hours = flights.getFlightHours())
                                                                print("{}{}, {} to {}, Depart {},\nArrive {}, Class {} Fare:${}".format(flights.getIATA(), flights.getOutbound(), flights.getOrigin() , flights.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'), keys ,flights.getFareAmount()[keys]))
                                                                
                                                    print("1 stopover, Total Fare depends on selected combination of seats")           
                                            else:
                                                no_seats_available_on_connecting = True


                                        if no_seats_available_on_direct == True and no_seats_available_on_connecting == True:
                                            print("\nNo flights available based on Trip details provided\n")
                                            no_seats_at_all = True



                                    elif user_input[4].lower() == "f":

                                        if len(list_of_matching_direct_flights) != 0:
                                            for items in list_of_matching_direct_flights:
                                                if len(items.getSeatsAvailableonFlight()["F"]) >= user_input[5]:
                                                    print("Result {}:".format(result_count))
                                                    results_dict["result {}".format(result_count)] = [items, "F"]
                                                    result_count +=1
                                                    departure_datetime = items.getDepartureDateTime()
                                                    arrival_datetime = items.getDepartureDateTime() + dt.timedelta(hours = items.getFlightHours())
                                                    print("{}{}, {} to {}, Depart {},\nArrive {}, Class F Fare:${}".format(items.getIATA(), items.getOutbound(), items.getOrigin() , items.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'),items.getFareAmount()["F"]))
                                                    print("0 stopover, Total Fare ${}".format(user_input[5] * items.getFareAmount()["F"]))
                                                    print_count = 1
                                                    
                                        if print_count != 1:
                                            no_seats_available_on_direct = True


                                        if len(pair_of_flights) != 0:
                                            flights_with_seats_on_connecting = []
                                            for items in pair_of_flights:
                                                count = 0
                                                for flights in items:
                                                    if len(flights.getSeatsAvailableonFlight()["F"]) >= user_input[5]:
                                                        count += 1
                                                        break

                                                if count == 2:
                                                    flights_with_seats_on_connecting.append(items)

                                            if len(flights_with_seats_on_connecting) != 0:
                                                for items in flights_with_seats_on_connecting:                                                
                                                    total_fare = 0
                                                    for flights in items:
                                                        if len(flights.getSeatsAvailableonFlight()["F"]) >= user_input[5]:
                                                            print("Result {}:".format(result_count))
                                                            results_dict["result {}".format(result_count)] = [flights, "F"]
                                                            result_count +=1
                                                            departure_datetime = flights.getDepartureDateTime()
                                                            arrival_datetime = flights.getDepartureDateTime() + dt.timedelta(hours = flights.getFlightHours())
                                                            print("{}{}, {} to {}, Depart {},\nArrive {}, Class F Fare:${}".format(flights.getIATA(), flights.getOutbound(), flights.getOrigin() , flights.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'), flights.getFareAmount()["F"]))
                                                            total_fare += flights.getFareAmount()["F"]
                                                    print("1 stopover, Total Fare ${}".format(user_input[5] * flights.getFareAmount()["F"]))           
                                            else:
                                                no_seats_available_on_connecting = True


                                        if no_seats_available_on_direct == True and no_seats_available_on_connecting == True:
                                            print("\nNo flights available on Cabin Class F based on Trip details provided\n")
                                            no_seats_at_all = True
                                
                                    elif user_input[4].lower() == "j":

                                        if len(list_of_matching_direct_flights) != 0:
                                            for items in list_of_matching_direct_flights:
                                                if len(items.getSeatsAvailableonFlight()["J"]) >= user_input[5]:
                                                    print("Result {}:".format(result_count))
                                                    results_dict["result {}".format(result_count)] = [items, "J"]
                                                    result_count +=1
                                                    departure_datetime = items.getDepartureDateTime()
                                                    arrival_datetime = items.getDepartureDateTime() + dt.timedelta(hours = items.getFlightHours())
                                                    print("{}{}, {} to {}, Depart {},\nArrive {}, Class J Fare:${}".format(items.getIATA(), items.getOutbound(), items.getOrigin() , items.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'),items.getFareAmount()["J"]))
                                                    print("0 stopover, Total Fare ${}".format(user_input[5] * items.getFareAmount()["J"]))
                                                    print_count = 1

                                        if print_count != 1:
                                            no_seats_available_on_direct = True


                                        if len(pair_of_flights) != 0:
                                            flights_with_seats_on_connecting = []
                                            for items in pair_of_flights:
                                                count = 0
                                                for flights in items:
                                                    if len(flights.getSeatsAvailableonFlight()["J"]) >= user_input[5]:
                                                        count += 1
                                                        break

                                                if count == 2:
                                                    flights_with_seats_on_connecting.append(items)

                                            if len(flights_with_seats_on_connecting) != 0:
                                                for items in flights_with_seats_on_connecting:                                                
                                                    total_fare = 0
                                                    for flights in items:
                                                        if len(flights.getSeatsAvailableonFlight()["J"]) >= user_input[5]:
                                                            print("Result {}:".format(result_count))
                                                            results_dict["result {}".format(result_count)] = [flights, "J"]
                                                            result_count +=1
                                                            departure_datetime = flights.getDepartureDateTime()
                                                            arrival_datetime = flights.getDepartureDateTime() + dt.timedelta(hours = flights.getFlightHours())
                                                            print("{}{}, {} to {}, Depart {},\nArrive {}, Class J Fare:${}".format(flights.getIATA(), flights.getOutbound(), flights.getOrigin() , flights.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'), flights.getFareAmount()["J"]))
                                                            total_fare += flights.getFareAmount()["J"]
                                                    print("1 stopover, Total Fare ${}".format(user_input[5] * flights.getFareAmount()["J"]))           
                                            else:
                                                no_seats_available_on_connecting = True


                                        if no_seats_available_on_direct == True and no_seats_available_on_connecting == True:
                                            print("\nNo flights available on Cabin Class J based on Trip details provided\n")
                                            no_seats_at_all = True




                                    elif user_input[4].lower() == "w":

                                        if len(list_of_matching_direct_flights) != 0:
                                            for items in list_of_matching_direct_flights:
                                                if len(items.getSeatsAvailableonFlight()["W"]) >= user_input[5]:
                                                    print("Result {}:".format(result_count))
                                                    results_dict["result {}".format(result_count)] = [items, "W"]
                                                    result_count +=1
                                                    departure_datetime = items.getDepartureDateTime()
                                                    arrival_datetime = items.getDepartureDateTime() + dt.timedelta(hours = items.getFlightHours())
                                                    print("{}{}, {} to {}, Depart {},\nArrive {}, Class W Fare:${}".format(items.getIATA(), items.getOutbound(), items.getOrigin() , items.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'),items.getFareAmount()["W"]))
                                                    print("0 stopover, Total Fare ${}".format(user_input[5] * items.getFareAmount()["W"]))
                                                    print_count = 1

                                        if print_count != 1:
                                            no_seats_available_on_direct = True

                                        if len(pair_of_flights) != 0:
                                            flights_with_seats_on_connecting = []
                                            for items in pair_of_flights:
                                                count = 0
                                                for flights in items:
                                                    if len(flights.getSeatsAvailableonFlight()["W"]) >= user_input[5]:
                                                        count += 1
                                                        break

                                                if count == 2:
                                                    flights_with_seats_on_connecting.append(items)

                                            if len(flights_with_seats_on_connecting) != 0:
                                                for items in flights_with_seats_on_connecting:                                                
                                                    total_fare = 0
                                                    for flights in items:
                                                        if len(flights.getSeatsAvailableonFlight()["W"]) >= user_input[5]:
                                                            print("Result {}:".format(result_count))
                                                            results_dict["result {}".format(result_count)] = [flights, "W"]
                                                            result_count +=1
                                                            departure_datetime = flights.getDepartureDateTime()
                                                            arrival_datetime = flights.getDepartureDateTime() + dt.timedelta(hours = flights.getFlightHours())
                                                            print("{}{}, {} to {}, Depart {},\nArrive {}, Class W Fare:${}".format(flights.getIATA(), flights.getOutbound(), flights.getOrigin() , flights.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'), flights.getFareAmount()["W"]))
                                                            total_fare += flights.getFareAmount()["W"]
                                                    print("1 stopover, Total Fare ${}".format(user_input[5] * flights.getFareAmount()["W"]))           
                                            else:
                                                no_seats_available_on_connecting = True


                                        if no_seats_available_on_direct == True and no_seats_available_on_connecting == True:
                                            print("\nNo flights available on Cabin Class W based on Trip details provided\n")
                                            no_seats_at_all = True


                                    elif user_input[4].lower() == "y":

                                        if len(list_of_matching_direct_flights) != 0:
                                            for items in list_of_matching_direct_flights:
                                                if len(items.getSeatsAvailableonFlight()["Y"]) >= user_input[5]:
                                                    print("Result {}:".format(result_count))
                                                    results_dict["result {}".format(result_count)] = [items, "Y"]
                                                    result_count +=1
                                                    departure_datetime = items.getDepartureDateTime()
                                                    arrival_datetime = items.getDepartureDateTime() + dt.timedelta(hours = items.getFlightHours())
                                                    print("{}{}, {} to {}, Depart {},\nArrive {}, Class Y Fare:${}".format(items.getIATA(), items.getOutbound(), items.getOrigin() , items.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'),items.getFareAmount()["Y"]))
                                                    print("0 stopover, Total Fare ${}".format(user_input[5] * items.getFareAmount()["Y"]))
                                                    print_count = 1

                                        if print_count != 1:
                                            no_seats_available_on_direct = True

                                        
                                        if len(pair_of_flights) != 0:
                                            flights_with_seats_on_connecting = []
                                            for items in pair_of_flights:
                                                count = 0
                                                for flights in items:
                                                    if len(flights.getSeatsAvailableonFlight()["Y"]) >= user_input[5]:
                                                        count += 1
                                                        break

                                                if count == 2:
                                                    flights_with_seats_on_connecting.append(items)

                                            if len(flights_with_seats_on_connecting) != 0:
                                                for items in flights_with_seats_on_connecting:                                                
                                                    total_fare = 0
                                                    for flights in items:
                                                        if len(flights.getSeatsAvailableonFlight()["Y"]) >= user_input[5]:
                                                            print("Result {}:".format(result_count))
                                                            results_dict["result {}".format(result_count)] = [flights, "Y"]
                                                            result_count +=1
                                                            departure_datetime = flights.getDepartureDateTime()
                                                            arrival_datetime = flights.getDepartureDateTime() + dt.timedelta(hours = flights.getFlightHours())
                                                            print("{}{}, {} to {}, Depart {},\nArrive {}, Class Y Fare:${}".format(flights.getIATA(), flights.getOutbound(), flights.getOrigin() , flights.getDestination(), departure_datetime.strftime('%d %b %y, %I:%M %p'),arrival_datetime.strftime('%d %b %y, %I:%M %p'), flights.getFareAmount()["Y"]))
                                                            total_fare += flights.getFareAmount()["Y"]
                                                    print("1 stopover, Total Fare ${}".format(user_input[5] * flights.getFareAmount()["Y"]))    
                                            else:
                                                no_seats_available_on_connecting = True

                                        if no_seats_available_on_direct == True and no_seats_available_on_connecting == True:
                                            print("\nNo flights available on Cabin Class Y based on Trip details provided\n")
                                            no_seats_at_all = True

                                    if no_seats_at_all == False:
                                        while True:
                                            user_input = input("Do you want to book a flight? Y/N\n").lower()

                                            if user_input == "n":
                                                break

                                            elif user_input == "y":
                                                user_input = input("Which available flight do you want to book? Please key in Result no. eg. Result 1\n").lower()

                                                if user_input not in list(results_dict.keys()):
                                                    print("You have selected an invalid result")
                                                
                                                else:
                                                    print("These are the available seats on the flight:")
                                                    print(results_dict[user_input][0].getSeatsAvailableonFlight()[results_dict[user_input][1]])
                                                    passenger_count = 0
                                                    for i in range(0, no_of_passengers):
                                                        passenger_count += 1
                                                        while True:
                                                            user_input_seats = input("Please select seat for Passenger {}\n".format(passenger_count))
                                                            if results_dict[user_input][1] not in list(results_dict[user_input][0].getBookedSeats().keys()):
                                                                results_dict[user_input][0].updateBookedSeats(results_dict[user_input][1], user_input_seats)
                                                                break
                                                            else:
                                                                if user_input_seats in results_dict[user_input][0].getBookedSeats()[results_dict[user_input][1]]:
                                                                    print("Selected seats already booked by another passenger, Please try another seat.")
                                                                    continue
                                                                else:
                                                                    results_dict[user_input][0].updateBookedSeats(results_dict[user_input][1], user_input_seats)
                                                                    break
                                                                                                                        
                                                        
                                                    
                                                    if passenger_count == no_of_passengers:
                                                        print("Your Flight is confirmed!")
                                                        break

                                                        

                                            else:
                                                print("\nERROR: You have entered an invalid input, Please try again\n")
                                                continue
                                        




        
        while True:
            
            user_input = input("\nDo you want to proceed with another action? Y/N\n").lower()
            
            if user_input in ["y", "n"]:

                break

            else:

                print("\nERROR: You have entered an invalid input, Please try again\n")
                continue

        if user_input == "y":
            
            continue

        elif user_input == "n":
            
            break




if __name__ == "__main__":
    main()