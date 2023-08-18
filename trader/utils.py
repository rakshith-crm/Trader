from tabulate import tabulate

WEEKS_TO_DAYS = {f'{i}wk': i * 7 for i in range(1, 4)}
MONTHS_TO_DAYS = {f'{i}mo': i * 30 for i in range(1, 12)}
YEARS_TO_DAYS = {f'{i}yr': 360 * i for i in range(1, 5)}
DAYS = {}
DAYS.update(WEEKS_TO_DAYS)
DAYS.update(MONTHS_TO_DAYS)
DAYS.update(YEARS_TO_DAYS)


def print_table(rows, headers=None):
    if headers:
        rows = [headers] + rows
        print(tabulate(rows, headers='firstrow', tablefmt='fancy_grid'))
    else:
        print(tabulate(rows, tablefmt='fancy_grid'))
