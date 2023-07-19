from tabulate import tabulate


def print_table(rows, headers=None):
    if headers:
        rows = [headers] + rows
        print(tabulate(rows, headers='firstrow', tablefmt='fancy_grid'))
    else:
        print(tabulate(rows, tablefmt='fancy_grid'))
