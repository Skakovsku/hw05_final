import datetime


def year(request):
    date_year = datetime.datetime.now()
    print(date_year.year)
    return {
        'year': date_year.year,
    }
