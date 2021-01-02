from datetime import date

def date_time_converter(o):
    if isinstance(o, date):
        return o.__str__()
