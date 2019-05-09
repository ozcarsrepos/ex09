#!/usr/bin/env python3

from stackexchange import StackOverflow
import sys  # NOQA
import argparse
import logging  # NOQA
# logger = log.get_logger(__name__)
logger = logging.getLogger(__name__)    # NOQA
logger.setLevel(logging.DEBUG)  # NOQA


def StackOverflow_result(n, label):
    so = StackOverflow()
    top_qs = so.questions(sort='votes', tagged=label, pagesize=n)
    if top_qs:
        print('Top {} questions from StackOverflow with tag {}'
              'as below:'.format(n, label))
        for o, q in enumerate(top_qs[:n], 1):
            print('{} - {}: {}'.format(o, q.title, q.link))
    else:
        sys.exit('Not found! Check your LABEL')


def main():
    parser = argparse.ArgumentParser(description="Get top N questions with"
                                     "tag LABEL from StackOverflow")
    parser.add_argument('num', metavar='N', type=int,
                        help='Input the integer number (N > 0) of top')
    parser.add_argument('label', metavar='LABEL', help='Input the LABEL'
                                                       'of questions to get')
    args = parser.parse_args()
    # Run if num is integer and num > 0
    if isinstance(args.num, int) and int(args.num) > 0:
        try:
            StackOverflow_result(args.num, args.label)
        except Exception as e:
            logger.debug('Appear exception:', e)
    else:
        sys.exit("N is integer number with minimum is 1")


if __name__ == '__main__':
    main()
