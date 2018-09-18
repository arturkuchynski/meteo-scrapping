import requests
from bs4 import BeautifulSoup
import sys
import xlsxwriter


class WeatherParser:

    def __init__(self, file):
        self.file = file

    def get_content(self, url):
        """
        Grab the content from web page
        :param url: meteo.by site url
        :return: page content as BeautifulSoup object
        """
        try:
            page = requests.get(url)
            page.raise_for_status()
            if page.status_code < 307:
                return BeautifulSoup(page.content, 'lxml')
            else:
                print('Error: {0}: {1} for url: {2}'.format(page.status_code, page.reason, page.url))
                sys.exit(1)

        except requests.exceptions.RequestException as ex:
            print("Error: " + str(ex))
            sys.exit(1)

    def get_forecast_decade(self, city):
        """
        Get the weather forecast for one decade
        :param city: string as city name for which the forecast data will be parsed
        """
        soup = self.get_content('https://meteo.by/{0}/'.format(city))

        # grab the forecast data from html tabs
        forecast_data = [[data.text.strip() for data in row_data.select('td')]
                         for row_data in soup.find_all('tr', {'class': 'time'})]

        for data in forecast_data:
            # remove whitespaces
            data[0] = ''.join(data[0].split())

        dates = soup.find_all('p', {'class': 'date'})
        date_list, temp = [], {}

        # fill the date list
        for date in dates:
            temp["Date"] = date.select("strong")[0].text
            temp["Month"] = date.text[4:]
            temp["Day"] = date.select("span")[0].text
            date_list.append(" ".join(list(temp.values())))

        dates = date_list

        if self.file:
            self._to_xl(dates, forecast_data, self.file)
        else:
            self._to_cli(dates, forecast_data)

    def _to_cli(self, dates, forecast):
        """
        Print retrieved forecast data on the console
        :param dates: list of decade dates
        :param forecast: list of lists of forecast data for each time of day for one decade
        """
        day_index, temp_index = 0, 0
        for quarter_index in range(0, len(forecast), 4):
            print("\n" + dates[day_index])
            day_index += 1
            if quarter_index > 0:
                for index in range(temp_index, quarter_index):
                    print(str(forecast[index]))

            temp_index = quarter_index

    def _to_xl(self, dates, forecast, path):
        """
        Write retrieved forecast data in .xlsx file
        :param dates: list of decade dates
        :param forecast: list of lists of forecast data for each time of day for one decade
        :param path: .xlsx file path
        """
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()

        worksheet.set_column(0, 5, 25)
        bold = workbook.add_format({'bold': 1})

        criteria = ['Температура min..max',
                    'Погода',
                    'Давление min..max',
                    'Влажность min..max',
                    'Ветер min..max',
                    'Направление']

        row, col = 0, 0
        for i in range(0, len(criteria)):
            worksheet.write_string(row, col + i, criteria[i], bold)

        day_index, temp_index, row = 0, 0, 1

        # loop through the forecast data
        for quarter_index in range(0, len(forecast), 4):
            # write the date for each day
            worksheet.write_string(row, 0, dates[day_index])

            if quarter_index > 0:
                # loop through the forecast for each time of day
                for index in range(temp_index, quarter_index):
                    row += 1
                    col = 0
                    for item in forecast[index]:
                        # write the data for each forecast criterion
                        worksheet.write_string(row, col, item)
                        col += 1
                temp_index = quarter_index
                day_index += 1
                row += 2

        workbook.close()
