from parsers.weather_parser import WeatherParser
import argparse
import sys
import re
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=False,
                    help="path to .xlsx file where the weather data will be stored")
    args = vars(ap.parse_args())
    file = Path(args["path"]).absolute() if args["path"] else None

    if file and not file.exists():
        print('File not found.\nPlease check if the file path was set correctly.')
        sys.exit(1)

    while True:
        city = input("Enter city name (latin chars only): ").lower()

        if re.match("[a-z]", city):
            break

    print("Processing your request...")
    wp = WeatherParser(file)
    wp.get_forecast_decade(city)
    print("DONE!")


if __name__ == "__main__":
    main()
