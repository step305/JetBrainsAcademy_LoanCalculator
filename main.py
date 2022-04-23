import math
import sys
import argparse
from argparse import RawTextHelpFormatter

HELP_TEXT = '''Hello! My name is Steven, and I am your personal assistant! These are the things I can do:
-- calculate of differentiated payments (type = diff). To do this you can run the program specifying:
                                    interest,
                                    number of monthly payments,
                                    loan principal.
-- calculate the values for annuity payment (principal loan, number of monthly payments, and monthly payment amount). 
You must specify known parameters - any 2 of principal loan, number of monthly payments, monthly payment amount and
                                            annual interest rate.
'''


def calc_annuity_periods(params):
    loan = int(params.principal)
    payment = int(params.payment)
    loan_interest = float(params.interest) / 100.0 / 12

    months_all = math.ceil(math.log(payment / (payment - loan_interest * loan), 1 + loan_interest))

    years = 0 if months_all < 12 else int(months_all / 12)
    months = int(months_all) % 12

    years_str = '' if years == 0 else ('1 year' if years == 1 else ' {} years'.format(years))
    months_str = '' if months == 0 else (' 1 month' if months == 1 else ' {} months'.format(months))

    return 'It will take' + years_str + months_str + ' to repay this loan!\n' + \
           'Overpayment = {:0.0f}'.format(payment * months_all - loan)


def calc_annuity_payment(params):
    loan = int(params.principal)
    months = int(params.periods)
    loan_interest = float(params.interest) / 100.0 / 12

    payment = math.ceil(loan * loan_interest * (1 + loan_interest) ** months / ((1 + loan_interest) ** months - 1))

    return 'Your monthly payment = {:0.0f}!\n'.format(payment) + \
           'Overpayment = {:0.0f}'.format(payment * months - loan)


def calc_annuity_princial(params):
    payment = float(params.payment)
    months = int(params.periods)
    loan_interest = float(params.interest) / 100.0 / 12

    loan = math.floor(payment / (loan_interest * (1 + loan_interest) ** months / ((1 + loan_interest) ** months - 1)))

    return 'Your loan principal = {:0.0f}\n'.format(loan) + \
           'Overpayment = {:0.0f}'.format(payment * months - loan)


def calc_diff_payments(params):
    mth_payments = []
    P = int(params.principal)
    n = int(params.periods)
    i = float(params.interest) / 12.0 / 100.0
    m = 1
    result = ''
    for m in range(1, n + 1):
        Dm = math.ceil(P / n + i * (P - P * (m - 1) / n))
        mth_payments.append(Dm)
        result = result + 'Month {:d}: payment is {:0.0f}\n'.format(m, Dm)
    result = result + 'Overpayment = {:0.0f}'.format(sum(mth_payments) - P)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=HELP_TEXT, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--type', help='indicates the type of payment: "annuity" or "diff" (differentiated). Required')
    parser.add_argument('--principal', help='the loan principal')
    parser.add_argument('--interest', help='annual interest rate')
    parser.add_argument('--periods', help='number of payments - the number of months in which repayments will be made')
    parser.add_argument('--payment', help='monthly payment')

    args = parser.parse_args()
    if args.type is None or not args.type in ['diff', 'annuity'] or len(sys.argv) < 5:
        print('Incorrect parameters')
        exit()

    if args.type == 'diff':
        if ((args.principal is None) or (int(args.principal) <= 0)
                or (args.interest is None) or (float(args.interest) <= 0)
                or (args.periods is None) or (int(args.periods) <= 0)):
            print('Incorrect parameters')
            exit()
        print(calc_diff_payments(args))

    elif args.type == 'annuity':
        if args.principal is None:
            if ((args.interest is None) or (float(args.interest) <= 0)
                    or (args.payment is None) or (int(args.payment) <= 0)
                    or (args.periods is None) or (int(args.periods) <= 0)):
                print('Incorrect parameters')
                exit()
            print(calc_annuity_princial(args))
        elif args.payment is None:
            if ((args.interest is None) or (float(args.interest) <= 0)
                    or (args.principal is None) or (int(args.principal) <= 0)
                    or (args.periods is None) or (int(args.periods) <= 0)):
                print('Incorrect parameters')
                exit()
            print(calc_annuity_payment(args))
        elif args.periods is None:
            if ((args.interest is None) or (float(args.interest) <= 0)
                    or (args.principal is None) or (int(args.principal) <= 0)
                    or (args.payment is None) or (int(args.payment) <= 0)):
                print('Incorrect parameters')
                exit()
            print(calc_annuity_periods(args))
        else:
            print('Incorrect parameters')
            exit()
