import datetime


def make_year_arr():
    date = datetime.date.today()
    year = date.strftime("%Y")
    options = ["전체"]
    options += [y for y in range(int(year), int(year) - 50, -1)]
    return options
