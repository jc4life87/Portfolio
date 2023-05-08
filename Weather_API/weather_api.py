import requests
import json
import math
import os


class Location:

    def __init__(self):
        self.city = ''
        self.zipcode = 0
        self.api_key = "59a453bce3fea33132f31d36aac93a15"
        self.country = 'US'
        self.digits = 0

    # Adds City Location to class
    def add_location(self, city):
        self.city = city

    # Adds zip code to class
    def add_zip_code(self, zipcode):
        self.zipcode = zipcode

    # Creates JSON file for city
    def get_weather_city(self):
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=imperial".format(self.city, self.api_key)
        get_weather = requests.get(url)
        if os.path.exists("weather.json"):  # Removes JSON to prevent returning old data
            os.remove("weather.json")
        weather = (get_weather.json())
        with open('weather.json', 'w') as outfile:  # Creates New JSON File
            json.dump(weather, outfile, indent=4)
        return

    # Creates JSON file for Zip Code
    def get_weather_zip_code(self):
        url = "https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}&units=imperial".format(self.zipcode, self.api_key)
        get_weather = requests.get(url)
        if os.path.exists("weather.json"):  # Removes JSON to prevent returning old data
            os.remove("weather.json")
        weather = (get_weather.json())
        with open('weather.json', 'w') as outfile:  # Creates New JSON File
            json.dump(weather, outfile, indent=4)
        return

    # Returns the length of Zip Code
    def zip_length(self):
        if self.zipcode > 0:
            self.digits = int(math.log10(self.zipcode))+1
        elif self.zipcode == 0:
            self.digits = 1
        else:
            self.digits = int(math.log10(-self.zipcode))+2
        return self.digits

    # Checks for the correct length of Zip Code and returns error code
    def zip_length_check(self):
        if self.digits < 5 or self.digits > 5:
            error = "Not a 5 digit zip code number"
        else:
            error = "Zip Code Good"
        return error

    # Checks JSON for 'COD' and returns error
    @staticmethod
    def check_errors():
        with open('weather.json') as json_file:
            data = json.load(json_file)
            cod = data.pop('cod')
            if cod == 200:
                error = "No errors"
            elif cod != 200:
                error = data.pop('message')
            return error

    # Parses the JSON file and returns the weather
    @staticmethod
    def get_weather():
        with open('weather.json') as json_file:
            data = json.load(json_file)
            # parsing the JSON file
            weather = data.pop('weather')
            items = data['main']
            city = data['name']
            temp = items.pop('temp')
            temp_max = items.pop('temp_max')
            temp_min = items.pop('temp_min')
            pressure = items.pop('pressure')
            humidity = items.pop('humidity')
            weather_desc = weather[0]
            weather_desc = weather_desc.pop('description')
            # printing to screen
            print('Here is the current weather in', city.capitalize())
            print('temperature:', temp)
            print('Maximum Temperature:', temp_max)
            print('Minimum Temperature: ', temp_min)
            print('Pressure:', pressure)
            print('Humidity:', humidity)
            print('Weather Description:', weather_desc)
        return


# Checking if city is an integer or string
def represents_int(value_int):
    try:
        int(value_int)
        return 'True'
    except ValueError:
        return value_int


def main():

    place = Location()
    print('Welcome to the daily weather program ')

    while True:

        try:
            print()
            selection = input('Please press 1 for weather by U.S. City'
                              ' or press 2 for zip code or type "Quit" to exit: ')
            value_error = 'False'
            if selection == '1':
                print()
                city = input('Please input U.S. City: ')
                value_int = city
                value = represents_int(value_int)
                if value == 'True':
                    value_error = 'True'
                    print("Input can't be numbers.")
                else:
                    city = value
                    place.add_location(city.capitalize())
            elif selection == '2':
                print()
                zipcode = int(input('Please input Zip Code: '))
                place.add_zip_code(zipcode)
                place.zip_length()
                zip_code_error = place.zip_length_check()
                if zip_code_error == "Zip Code Good":
                    continue
                elif zip_code_error == "Not a 5 digit zip code number":
                    print(zip_code_error)
            elif selection.startswith(('q', 'Q')):
                print()
                print('Thanks for visiting!')
                break

        except ValueError:
            value_error = 'True'
            if value_error == 'True':
                print('That was not a valid response')
            else:
                continue

        finally:
            if value_error == 'True':
                continue
            elif value_error == 'False':
                if selection == '1':
                    place.get_weather_city()
                    error = place.check_errors()
                    if error == 'No errors':
                        place.get_weather()
                    else:
                        print(error)
                elif selection == '2':
                    place.get_weather_zip_code()
                    error = place.check_errors()
                    if error == 'No errors':
                        place.get_weather()
                    else:
                        print(error)


# Calls main function
if __name__ == "__main__":
    main()
