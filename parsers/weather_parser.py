import requests
from bs4 import BeautifulSoup
import pandas


class WeatherParser:

    @staticmethod
    def get_forecast_local_today():
        """
        Gets the local weather forecast and saves It to .txt file
        """
        page = requests.get('https://meteo.by/')

        # success
        if page.ok:
            soup = BeautifulSoup(page.content, 'lxml')
            data = {}

            # get the current date
            p = soup.find('p', {"class": "c"})
            data["Город"] = p.select("strong")[0].text
            data["Дата"] = p.select("small")[0].text
            data["Время"] = p.select("small")[1].text

            # get local temperature
            p = soup.find('p', {"class": 't'})
            # remove whitespaces
            data["Температура"] = p.select("strong")[0].text.strip().replace('\r\n                        ', '')

            # get forecast
            p = soup.find('p', {"class": 's'})
            data["Погода"] = p.text.strip()

            df = pandas.DataFrame.from_dict(data, orient='index', columns=['Прогноз для:'])

            with open("out/local.txt", "w") as file:
                file.write(df.to_string())

        else:
            # if page rendered with an error code, save the error code
            if page.status_code >= 400:
                err_message = "Error " + str(page.status_code)
                print(err_message)
                with open("out/local.txt", "w") as file:
                    file.write(err_message)

    @staticmethod
    def get_forecast_rss_today(city):
        """
        Gets the weather forecast from rss feed for given city

        :param city: string as city name for which the forecast data will be parsed
        """
        page = requests.get('https://meteo.by/{0}/rss/'.format(city))

        if page.ok:
            soup = BeautifulSoup(page.text, 'lxml')
            td = [[data.text.strip() for data in row_data.select('td')]
                  for row_data in soup.find_all('tr')[2:-1:]]

            for data in td:
                # remove whitespaces
                data[0] = data[0].replace("\r\n                            ", ' ')

            df = pandas.DataFrame(td,
                                  columns=['Температура',
                                           'Прогноз',
                                           'Давление',
                                           'Влажность',
                                           'Ветер',
                                           'Направление'])

            # serialize the data
            df.to_csv("out/{0}_rss.csv".format(city))
            with open("out/{0}_rss.txt".format(city), "w") as file:
                file.write(df.to_string())


        else:
            if page.status_code >= 400:
                err_message = "Error " + str(page.status_code)
                print(err_message)
                with open("out/{0}_rss.txt".format(city), "w") as file:
                    file.write(err_message)

    @staticmethod
    def get_forecast_decade(city):
        """
        Get the weather forecast for the one decade for given city

        :param city: string as city name for which the forecast data will be parsed
        """
        page = requests.get('https://meteo.by/{0}/'.format(city))

        if page.ok:
            soup = BeautifulSoup(page.content, 'lxml')

            td = [[data.text.strip() for data in row_data.select('td')]
                  for row_data in soup.find_all('tr', {'class': 'time'})]

            for data in td:
                # remove whitespaces
                data[0] = data[0].replace("\r\n                            ", ' ')

            dates = soup.find_all('p', {'class': 'date'})

            date_list, temp = [], {}

            for date in dates:
                temp["Date"] = date.select("strong")[0].text
                temp["Month"] = date.text[4:]
                temp["Day"] = date.select("span")[0].text

                date_list.append(" ".join(list(temp.values())))

            df = pandas.DataFrame(td, columns=['Температура',
                                               'Прогноз',
                                               'Давление min…max',
                                               'Влажность min…max',
                                               'Ветер',
                                               'Направление'])

            with open("out/{0}_decade.txt".format(city), "w") as file:
                i = 0
                # group weather data for each day according to the time of day
                for n in range(0, len(df), 4):
                    file.write(str(date_list[i]) + "\n")
                    file.write(df[n:n + 4:].to_string() + "\n\n")
                    i += 1

        else:
            if page.status_code >= 400:
                err_message = "Error " + str(page.status_code)
                print(err_message)
                with open("out/{0}_rss.txt".format(city), "w") as file:
                    file.write(err_message)
