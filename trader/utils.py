from tabulate import tabulate

WEEKS_TO_DAYS = {f"{i}wk": i * 7 for i in range(1, 4)}
MONTHS_TO_DAYS = {f"{i}mo": i * 30 for i in range(1, 12)}
YEARS_TO_DAYS = {f"{i}yr": 360 * i for i in range(1, 5)}
DAYS = {}
DAYS.update(WEEKS_TO_DAYS)
DAYS.update(MONTHS_TO_DAYS)
DAYS.update(YEARS_TO_DAYS)


def print_table(rows, headers=None):
    if headers:
        rows = [headers] + rows
        print(tabulate(rows, headers="firstrow", tablefmt="fancy_grid"))
    else:
        print(tabulate(rows, tablefmt="fancy_grid"))


def are_numbers_close(number1, number2):
    absolute_difference = abs(number1 - number2)
    average = (number1 + number2) / 2

    relative_difference = absolute_difference / average

    # Define a threshold for closeness (e.g., 0.1 for 10%)
    threshold = 0.03  # Adjust this threshold as needed

    if relative_difference < threshold:
        return True
    else:
        return False
