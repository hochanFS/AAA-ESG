import datetime
# import xml
from http import client
import logging

RELIABLE_WEBSITE1 = "www.google.com"
RELIABLE_WEBSITE2 = "www.amazon.com"


class InternetConnectionChecker(object):
    """
    This class helps determine whether we have access to web page.
    Since checking whether we have overall access to the Internet every time we initialize the class can be expensive,
    this class follows the Singleton design pattern.
    """
    __instance = None

    def __init__(self, do_not_throw_error: bool = False):
        """
        :param do_not_throw_error: whether no Internet connection should throw an error (False)
            or report with logging (True)
        """
        if InternetConnectionChecker.__instance is None:
            self._do_not_throw_error = do_not_throw_error
            if not InternetConnectionChecker.can_access_website():
                if not do_not_throw_error:
                    raise OSError("Unable to connect... Please check the Internet connection")
                else:
                    logging.warning("Unable to connect... Please check the Internet connection")
            InternetConnectionChecker.__instance = self
        else:
            self._do_not_throw_error = do_not_throw_error

    @staticmethod
    def get_instance(do_not_throw_error: bool = False):
        """
        Call the initializer if we haven't used the class before, or return the instance we called earlier
        :param do_not_throw_error: whether no Internet connection should throw an error (False)
            or report with logging (True)
        :return: the configured instance of Numerix Object's headers and relations
        """
        if InternetConnectionChecker.__instance is None\
                or InternetConnectionChecker.__instance.do_not_throw_error == do_not_throw_error:
            InternetConnectionChecker(do_not_throw_error)
        return InternetConnectionChecker.__instance

    @staticmethod
    def can_access_website(address: str = None) -> bool:
        """
        Checks whether the Internet can be accessed
        :param address: the URL address of the target Internet; if not specified, the method checks whether
            the access to general Internet is available
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
    def do_not_throw_error(self):
        return self._do_not_throw_error


class __CloudImporter(object):
    def __init__(self):
        pass

    def pull_data(self, date: datetime.date):
        if not isinstance(date, datetime.date):
            raise ValueError("date must be of type datetime.date")


class CommunityYieldCurveImporter(__CloudImporter):
    def __init__(self):
        super().__init__()

    def pull_data(self, date: datetime.date):
        """
        Pull the data from online source
        :param date:
        :return:
        """
        super(CommunityYieldCurveImporter, self).pull_data(date)


if __name__ == "__main__":
    pass
