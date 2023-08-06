# Local package imports.
from tsofa._views._dbse_prd import Command as BC


class Command(BC):

    # Set the platform, report, and date data endpoint for a time
    # resolution in seconds.
    default_endpoint = '/_design/dsec-prd/_view/dsec-prd/queries'


def main():
    Command.run()

