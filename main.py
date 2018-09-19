from parsers.weather_parser import WeatherParser
from utils.argparser import parse_file
import re


def main():
    file = parse_file('XLSX')

    while True:
        city = input("Enter city name (latin chars only): ").lower()

        if re.match("[a-z]", city):
            break

    print("Processing your request...")
    wp = WeatherParser(file)
    wp.get_forecast_decade(city)
    print("\nDone!")


if __name__ == "__main__":
    main()
