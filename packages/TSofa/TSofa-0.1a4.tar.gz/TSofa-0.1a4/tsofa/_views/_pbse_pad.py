# Standard library imports.
from argparse import ArgumentTypeError as ATE

# Local package imports.
from tsofa._views._base import Command as BC


class Command(BC):

    # Set the templates for dates to empty.  Only datetimes will be
    # parsed.
    tmpls_dates = []

    # The parameters accepted by the "gen_query" method.
    pnames = ('pid', 'attr', 'sdate', 'edate', 'desc', 'limit')

    # The Javascript view emits keys containing the platform ID, the
    # platform attribute ID, and a date component.  The emitted value
    # should be a Javascript object.
    #
    # THIS IS NOT A VALID ENDPOINT.  The endpoint is shown as an
    # example.  Set the correct endpoint in the child classes.
    default_endpoint = '/_design/pbse-pad/_view/pbse-pad/queries'

    # The date component of the returned keys starts after the platform
    # ID and the platform attribute ID values.
    key_date_index = 2

    def arg_param(self, param):

        param = BC.arg_param(self, param)

        for a in ('pid', 'attr',):

            if a in param.keys():
                if type(param[a]) != type(''):
                    raise ATE('{} must be string'.format(a))

            else:
                raise ATE('{} is required'.format(a))

        if type(param.get('desc', False)) != type(True):
            raise ATE('desc must be a boolean value')

        if type(param.get('limit', 0)) != type(0):
            raise ATE('limit must be an integer')

        return param

    @staticmethod
    def gen_query(pid, attr, sdate, edate, **kwargs):

        query = {'reduce': 'false'}

        # Create the start and end key "arrays" for the query,
        # populating the first two elements with the platform ID and the
        # platform attribute ID.
        query['startkey'] = [pid, attr]
        query['endkey'] = [pid, attr]

        # Generate the date components for the start and end keys,
        # joining them with the platform ID and attribute ID values.
        # Swap the keys if the descending flag is set.
        if kwargs.get('desc', False) == True:

            query['startkey'] += BC.gen_date_key(edate) + ['\ufff0']
            query['endkey'] += BC.gen_date_key(sdate)
            query['descending'] = 'true'

        else:

            query['startkey'] += BC.gen_date_key(sdate)
            query['endkey'] += BC.gen_date_key(edate) + ['\ufff0']

        # Limit the output to a given number of JSON documents.
        if type(kwargs.get('limit', None)) == type(0):
            if kwargs['limit'] > 0:
                query['limit'] = kwargs['limit']

        return query

