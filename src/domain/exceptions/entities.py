from src.common.exceptions.common import CommonException


class EntitiesException(CommonException):
    data: str

    @property
    def message(self):
        return "Base entity exception"


class ProductLengthTooShortException(CommonException):
    data: str

    @property
    def message(self):
        return f"Product name too shot exception {len(self.data) < 1}"


class ProductLengthTooLongException(CommonException):
    data: str

    @property
    def message(self):
        return f"Product name too long exception {len(self.data) > 100}"


class TooSmallQuantityException(CommonException):
    data: str

    @property
    def message(self):
        return f"Quantity too small exception {self.data} <= 0"


class TooSmallPriceException(CommonException):
    data: str

    @property
    def message(self):
        return f"Price too small exception {self.data} < 0"
