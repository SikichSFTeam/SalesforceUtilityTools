import datetime


class SfData(object):
    required = False
    externalId = False
    unique = False
    value = None

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def __str__(self):
        return str(self.value) if self.value is not None else None

    def to_json(self):
        return self.__str__()

class SfText(SfData):
    length = 0

    def __init__(self, length=250, *args, **kwargs):
        self.length = length
        return super().__init__(*args, **kwargs)

    def to_json(self):
        return self.__str__()

class SfDate(SfData):

    def __setattr__(self, name, value):
        if name == 'value':
            if isinstance(value, datetime.datetime):
               value = value.date()

        return super().__setattr__(name, value)

    def __str__(self):
        if self.value is None:
            return None
        else:
            return self.value.isoformat()

    def to_json(self):
        return self.__str__()

class SfDatetime(SfData):

    def __setattr__(self, name, value):
        if name == 'value':
            if isinstance(value, datetime.date):
               value = datetime.datetime(value.year, value.month, value.day,0,0,0,0,None)

        return super().__setattr__(name, value)

    def __str__(self):
        if self.value is None:
            return None
        else:
            return self.value.isoformat()

    def to_json(self):
        return self.__str__()

class SfNumeric(SfData):
    precision = 0
    scale = 0

    def __init__(self, precision=0, scale=0, *args, **kwargs):
        self.precision = precision
        self.scale = scale
        return super().__init__(*args, **kwargs)


class SfBool(SfData):

    def __setattr__(self, name, value):
        if name == 'value':
            if value in ['Yes', 'yes', 'Y', 'y', 'True', 'true', True, 1]:
                value = True
            else:
                value = False

        return super().__setattr__(name, value)

    def __str__(self):
        return 'true' if data else 'false'

    def to_json(self):
        self.__str__()