# Local package imports.
from tsofa._views._pbse_pad import Command as BC


class Command(BC):

    # Set the platform, attribute, and date platform metadata endpoint
    # for a time resolution in seconds.
    default_endpoint = '/_design/psec-pad/_view/psec-pad/queries'


def main():
    Command.run()

