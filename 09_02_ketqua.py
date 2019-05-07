#!/usr/bin/env python3

from requests_html import HTMLSession as html
from copy import deepcopy
import argparse
import sys
import logging  # NOQA
# logger = log.get_logger(__name__)
logger = logging.getLogger(__name__)    # NOQA
logger.setLevel(logging.DEBUG)  # NOQA


# Get the results from ketqua.net (special to 7nd prizes and lô-prize)
def ketqua_prizes():
    ses = html()
    resp = ses.get('https://ketqua.net')
    prize_nums = {'Đặc biệt': 1, 'Nhất': 1, 'Nhì': 2, 'Ba': 6, 'Tư': 4,
                  'Năm': 6, 'Sáu': 3, 'Bảy': 4}
    result = deepcopy(prize_nums)
    result['Lô'] = []
    for order, (prize, num) in enumerate(prize_nums.items()):
        result[prize] = []
        # Search and append prize in element with id = 'rs_...', eg: "rs_0_0"
        for i in range(num):
            id = '_'.join(['#rs', str(order), str(i)])
            prz = resp.html.find(id, first=True).text
            result[prize].append(prz)
            result['Lô'].append(prz[-2:])
    return result


# Check if the numbers will be gotten lô-prize, else: print prizes
def check_prize(*nums):
    win = False
    result = ketqua_prizes()
    if nums:
        for num in nums:
            num = str(num).zfill(2)
            if num in result['Lô']:
                print('Chúc mừng! Số {} trúng'.format(num))
                win = True
    if not win:
        print('Không có số trúng, kết quả xổ số như sau:')
        for prize, num in result.items():
            if prize != 'Lô':
                print('\nGiải {}:'.format(prize), end='\t')
                for n in num:
                    print(n, end='\t')


def main():
    if len(sys.argv) == 1:
        check_prize()
    else:
        parser = argparse.ArgumentParser(description="Kiểm tra kết quả "
                                         "xổ số - lô")
        parser.add_argument('nums', metavar='N', type=int, nargs='+',
                            choices=range(100), help='Nhập các số dương'
                            ' có 2 chữ số để kiểm tra lô')
        args = parser.parse_args()
        check_prize(*args.nums)


if __name__ == '__main__':
    main()
