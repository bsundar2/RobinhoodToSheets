import argparse
from src.rh_portfolio_to_sheets import export_rh_portfolio_to_sheets


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--live", help="Live connection to Robinhood to get portfolio data",
                        action="store_true")
    parser.add_argument("-w", "--write-mock", help="Write portfolio data to mock JSON file",
                        action="store_true")
    args = parser.parse_args()

    export_rh_portfolio_to_sheets(args.live, args.write_mock)
