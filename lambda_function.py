from src.rh_portfolio_to_sheets import export_rh_portfolio_to_sheets


def lambda_handler(event, context):
    print("Running lambda function")
    export_rh_portfolio_to_sheets(is_live=True, write_mock=False)
