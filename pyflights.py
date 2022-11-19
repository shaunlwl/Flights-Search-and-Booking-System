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

                if len(user_input) == 10 or len(user_input) == 9:
                    

                    #Get Fare Amount input once data validation are done
                    user_input = input("\nPlease Input Fare Amount by Cabin Class separated by commas. Eg. Cabin Class F - $2000, Cabin Class J - $1000, Cabin Class Y - $500\n")


                else:                       
                    print("\nERROR: You have entered an invalid amount of inputs, Please try again")


            if user_input == "4": #Search and Book Flight
                pass


        
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