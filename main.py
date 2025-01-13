import argparse
from src.rh_portfolio_to_sheets import export_rh_portfolio_to_sheets

def scratchpad():
    print("Executing scratchpad code.")
    print("Done executing scratchpad code.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--live",
        help="Live connection to Robinhood to get portfolio data",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-w",
        "--write-mock",
        help="Write portfolio data to mock JSON file",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--scratchpad",
        help="Run code in scratchpad",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    if not args.scratchpad:
        export_rh_portfolio_to_sheets(args.live, args.write_mock)
    else:
        scratchpad()
