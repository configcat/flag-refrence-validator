import argparse
import logging
import sys

from utils.config_fetcher import ConfigFetcher
from utils.reference_finder import ReferenceFinder
from utils.reference_validator import ReferenceValidator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("api_key",
                        help="The api key for your ConfigCat project.")
    parser.add_argument("search_dir",
                        help="The directory to scan for flag references.")
    parser.add_argument("-b", "--base_url",
                        help="The base url for your ConfigCat configuration file.",
                        default="cdn.configcat.com")
    parser.add_argument("-f", "--fail",
                        help="Signals an error when the validation fails, by default only warnings are showed.",
                        default=False,
                        const=True,
                        nargs='?',
                        type=str2bool)
    parser.add_argument("-v", "--verbose",
                        default=False,
                        const=True,
                        nargs='?',
                        help="Turns on detailed logging",
                        )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    fetcher = ConfigFetcher(args.api_key, args.base_url)
    finder = ReferenceFinder(args.search_dir)

    if not ReferenceValidator.validate(set(fetcher.get_flag_keys()), finder.find_references()) and args.fail:
        sys.exit(1)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    main()
