import datetime
import urllib3
import xmltodict
from http import client
import logging
from collections import OrderedDict
import math

RELIABLE_WEBSITE1 = "www.google.com"
RELIABLE_WEBSITE2 = "www.amazon.com"


class InternetConnectionChecker(object):
    """
    This class helps determine whether we have access to web page.
    Since checking whether we have overall access to the Internet every time we initialize the class can be expensive,
    this class follows the Singleton design pattern.
    """
    __instance = None

    def __init__(self, suppress_error: bool = False):
        """
        :param suppress_error: whether no Internet connection should throw an error (False)
            or report with logging (True)
        """
        self._suppress_error = suppress_error
        if InternetConnectionChecker.__instance is None:
            if InternetConnectionChecker.can_access_website():
                self._has_internet_access = True
                InternetConnectionChecker.__instance = self
                # once we check there is an internet connection, we do not recheck
            else:
                self._has_internet_access = False
                if not suppress_error:
                    raise OSError("Unable to connect... Please check the Internet connection")
                else:
                    logging.warning("Unable to connect... Please check the Internet connection")

    @staticmethod
    def get_instance(suppress_error: bool = False):
        """
        Call the initializer if we haven't used the class before, or return the instance we called earlier
        :param suppress_error: whether no Internet connection should throw an error (False)
            or report with logging (True)
        :return: the configured instance of Numerix Object's headers and relations
        """
        if InternetConnectionChecker.__instance is None\
                or InternetConnectionChecker.__instance.suppress_error == suppress_error:
            InternetConnectionChecker(suppress_error)
        return InternetConnectionChecker.__instance

    @staticmethod
    def can_access_website(address: str = None) -> bool:
        """
        Checks whether the Internet can be accessed
        :param address: the URL address we want to test whether it is accessible;
            if not specified, the method checks whether the machine can access to reliable websites
        :return: True if connection is successful; False otherwise
        """
        if address is None:
            return InternetConnectionChecker.can_access_website(RELIABLE_WEBSITE1) or \
                   InternetConnectionChecker.can_access_website(RELIABLE_WEBSITE2)
        connection = client.HTTPConnection(address, timeout=5)
        try:
            connection.request("HEAD", "/")
            connection.close()
            return True
        except OSError:
            connection.close()
            return False

    @property
    def has_internet_access(self):
        return self._has_internet_access

    @property
    def do_not_throw_error(self):
        return self._suppress_error


class __CloudImporter(object):
    def __init__(self):
        self.internet_access_checker = InternetConnectionChecker.get_instance(suppress_error=False)

    def pull_data(self, date: datetime.date):
        if not isinstance(date, datetime.date):
            raise ValueError("date must be of type datetime.date")
        if date > date.today():
            raise ValueError("The date parameter cannot be a future date.")
        if date.year < 2010:
            raise ValueError("The date should be later than year 2010.")


class CommunityTreasuryCurveImporter(__CloudImporter):
    XML_URL = "https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20{}"
    HEADER1 = 'feed'
    HEADER2 = 'entry'
    HEADER3 = 'content'
    HEADER4 = 'm:properties'
    HEADER5 = '#text'
    DATE_NAVIGATION = [HEADER3, HEADER4, 'd:NEW_DATE', HEADER5]
    DATA_KEY = ['d:BC_1MONTH', 'd:BC_2MONTH', 'd:BC_3MONTH', 'd:BC_6MONTH', 'd:BC_1YEAR', 'd:BC_2YEAR',
                'd:BC_3YEAR', 'd:BC_5YEAR', 'd:BC_7YEAR', 'd:BC_10YEAR', 'd:BC_20YEAR', 'd:BC_30YEAR']
    CLEAN_KEY =['1M', '2M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y']

    def __init__(self):
        super().__init__()

    def __pull_data_from_previous_market_date(self, date: datetime.date, desired_date: datetime.date):
        logging.warning("Market is not available on {}. Fetching market data on {} instead.".format(desired_date, date))
        return self.pull_data(date)

    def pull_data(self, date: datetime.date) -> dict:
        """
        Imports Treasury rates from https://data.treasury.gov for a particular date
        :param date: the date of our interest for fetching market data
            *NOTE* If the date is not available, this fetch the market data for the last available, closest date
        :return: dictionary with {key=tenor: value=interest rate}
        """
        super(CommunityTreasuryCurveImporter, self).pull_data(date)
        url = CommunityTreasuryCurveImporter.XML_URL.format(date.year)
        http = urllib3.PoolManager()
        http_response = http.request('GET', url)
        cleaned_data = dict()
        dict_value = xmltodict.parse(http_response.data)[self.HEADER1][self.HEADER2]
        index_guess = min(max(0, (date.month - 1) * 20 + int(date.day * 5 / 7)), len(dict_value) - 1)
        # Improve look-up speed by providing a good initial guess. Binary search may or may not be faster.

        # Identify the corresponding index i for the specified date
        i = index_guess
        found_greater_than_date = i == len(dict_value)
        found_less_than_date = i == 0
        closest_date = None
        while not found_greater_than_date and not found_less_than_date:
            if i == -1:
                return self.__pull_data_from_previous_market_date(datetime.date(date.year - 1, 12, 31), date)
            if i == len(dict_value):
                return self.__pull_data_from_previous_market_date(closest_date, date)
            temp = dict_value[i]
            for nav in CommunityTreasuryCurveImporter.DATE_NAVIGATION:
                temp = temp[nav]
            index_date = datetime.datetime.strptime(temp, '%Y-%m-%dT%H:%M:%S').date()
            if index_date == date:
                return self._construct_market_data_dict(dictionary_val=dict_value[i][self.HEADER3][self.HEADER4])
            if index_date < date:
                found_less_than_date = True
                closest_date = index_date
                i += 1
                continue
            if index_date > date:
                found_greater_than_date = True
                i -= 1
        return self.__pull_data_from_previous_market_date(closest_date, date)

    @staticmethod
    def _construct_market_data_dict(dictionary_val: dict):
        cleaned_data = OrderedDict()
        i = 0
        for key_name in CommunityTreasuryCurveImporter.DATA_KEY:
            if key_name in dictionary_val.keys():
                cleaned_data.setdefault(CommunityTreasuryCurveImporter.CLEAN_KEY[i], int(
                                        float(dictionary_val[key_name][CommunityTreasuryCurveImporter.HEADER5]) * 10000)
                                        / 1000000.0)
            else:
                cleaned_data.setdefault(CommunityTreasuryCurveImporter.CLEAN_KEY[i], None)
            i += 1
        return cleaned_data


if __name__ == "__main__":
    treasury = CommunityTreasuryCurveImporter()
    print(treasury.pull_data(datetime.date(2020, 2, 7)))
