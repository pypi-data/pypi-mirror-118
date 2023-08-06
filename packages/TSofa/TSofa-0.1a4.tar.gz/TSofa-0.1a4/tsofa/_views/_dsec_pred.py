# Local package imports.
from tsofa._views._dbse_pred import Command as BC


class Command(BC):

    # Set the platform, report, element, and date data endpoint for a
    # time resolution in seconds.
    default_endpoint = '/_design/dsec-pred/_view/dsec-pred/queries'


def main():
    Command.run()

