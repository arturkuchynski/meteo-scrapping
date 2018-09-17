from parsers.weather_parser import WeatherParser
import re


def main():
    while True:
        city = input("Enter city name (latin chars only): ").lower()

        if re.match("[a-z]", city):
            break

    wp = WeatherParser()

    print("Processing your request...")
    wp.get_forecast_local_today()
    wp.get_forecast_rss_today(city)
    wp.get_forecast_decade(city)
    print("DONE!\nCheck the output file!")


if __name__ == "__main__":
    main()
