from datetime import date, timedelta
from argparse import ArgumentParser, Namespace


def calc_between(start: date, end: date, inclusive: bool) -> int:
    sign = 1 if start <= end else -1
    numberDays = end - start + timedelta(sign*(not inclusive))
    return numberDays.days


def calc_workdays_between(start: date, end: date, inclusive: bool) -> int:
    sign = 1 if start <= end else -1
    start = start + timedelta(sign*(inclusive))

    if start.weekday() in [5, 6]:
        start += timedelta(abs(start.weekday() - 7))
    if end.weekday() in [5, 6]:
        end -= timedelta(abs(7 - end.weekday()))

    time_between = end - start
    weeks = int(time_between.days/7)

    numberDays = weeks * 5 + abs(end.weekday() + (5 - start.weekday())) % 5 + 1

    return numberDays


def parse_args() -> Namespace:
    parser = ArgumentParser(
        prog='Time Between', description='Calculate the number of days between two dates.')
    parser.add_argument('-m', type=int, help='End Date Month')
    parser.add_argument('-d', type=int, help='End Date Day')
    parser.add_argument('-y', type=int, help='End Date Year')
    parser.add_argument('-w', '--workdays',
                        action='store_true', help='Only count workdays')
    parser.add_argument('-I', '--notInclusive',
                        action='store_true', help='Don\'t count today in total')
    parser.add_argument('-S', '--setStart', metavar=('MM', 'DD', 'YYYY'), type=int, nargs=3,
                        help='Specify Start')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    return parser.parse_args()


def main():
    args = parse_args()

    start = date.today()
    if args.setStart:
        start = date(args.setStart[2], args.setStart[0], args.setStart[1])

    if args.d is None:
        args.d = 1
    if args.y is None:
        args.y = start.year
    if args.m is None:
        args.m = start.month

    given_date = date(args.y, args.m, args.d)

    func = calc_between
    if args.workdays:
        func = calc_workdays_between

    print(func(start, given_date, args.notInclusive))


if __name__ == '__main__':
    main()
