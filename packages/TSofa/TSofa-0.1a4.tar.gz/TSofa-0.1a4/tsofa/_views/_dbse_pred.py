# Standard library imports.
import datetime
from argparse import ArgumentTypeError as ATE

# Local package imports.
from tsofa._views._base import Command as BC


# List the parameter names used to construct a database query.
PNAMES = ('pid', 'rpt', 'elm', 'sdate', 'edate', 'desc', 'limit', 'reduce')


class Command(BC):

    # Set the templates for dates to empty.  Only datetimes will be
    # parsed.
    tmpls_dates = []

    # The gen_query method below accepts only the argument names defined
    # in the above "PNAMES".
    pnames = PNAMES

    # The Javascript view emits keys containing the platform ID, data
    # report ID, the data element ID and a date component.  The value
    # emitted should be a numerical value.
    #
    # THIS IS NOT A VALID ENDPOINT.  The endpoint is shown as an
    # example.  Set the correct endpoint in the child classes.
    default_endpoint = '/_design/dbse-pred/_view/dbse-pred/queries'

    # The date component of the returned keys starts after the platform
    # ID, the data report ID, and the data element ID values.
    key_date_index = 3

    def _rsmp(self, pid, rpt, elm, sdate, edate, td, eoi, ins, ine):

        # A list of expanded parameters based on the number of date and
        # time intervals between the start and end date ranges.
        expanded = []

        # Count the number of date and time intervals.
        count = 0

        # Generate a param dictionary for every given day.
        while sdate <= edate:

            np = {'pid': pid, 'rpt': rpt, 'elm': elm, 'reduce': True}

            # Specifies that the given day is the end of the daily reporting
            # period, so the day is used as the endpoint of the day data
            # request.
            if eoi == True:

                sd = sdate - td
                ed = sdate

            else:

                sd = sdate
                ed = sdate + td

            # Now, adjust the endpoints of the date range defined by the
            # datetime objects above.
            if ins == False:
                sd += datetime.timedelta(seconds = 1)

            if ine == False:
                ed -= datetime.timedelta(seconds = 1)

            # Add the adjusted start and end dates to the new param
            # dictionary.
            np.update({'sdate': sd, 'edate': ed})

            # Finally add the new parameter dictionary to the params
            # list.
            expanded.append(np)

            # Increment the counter and the adjust the sdate to the next
            # date and time interval.
            count += 1
            sdate += td

        return (expanded, count)

    def arg_param(self, param):

        param = BC.arg_param(self, param)

        for a in ('pid', 'rpt', 'elm',):

            if a in param.keys():
                if type(param[a]) != type(''):
                    raise ATE('{} must be string'.format(a))

            else:
                raise ATE('{} is required'.format(a))

        for a in ('desc', 'reduce'):
            if type(param.get(a, False)) != type(True):
                raise ATE('{} must be a boolean value'.format(a))

        if type(param.get('limit', 0)) != type(0):
            raise ATE('limit must be an integer')

        if type(param.get('rsmp', '')) != type(''):
            raise ATE('rsmp must be a string literal')

        return param

    def handle(self, *args, **kwargs):

        # The return value.
        data = []

        # Depending on the reduction code, each given param dictionary
        # will be expanded to include every time interval between the
        # original start and end dates.
        expanded_params = []

        for param in kwargs['params']:

            # Resampling method keyword arguments are defined here.
            rka = {}

            for k in ('pid', 'rpt', 'elm', 'sdate', 'edate'):
                rka[k] = param.get(k, '')

            # This is the resampling code, specifying the type of
            # resampling and the inclusion/exclusion rules.
            rc = str(param.get('rsmp', ''))

            # Determine if the resampled dates specify data before the
            # date, or after the date.  In other words, do the dates
            # specify a report at the end of the resampled interval, or
            # at the beginnning.
            rka['eoi'] = False

            if rc.startswith('-'):

                rc = rc[1:]
                rka['eoi'] = True

            # Now, get the inclusive/exclusive flags for the endpoints
            # of the resampled interval.
            rka['ins'] = True
            rka['ine'] = False

            # Exclude the start.
            if rc.startswith('X') == True:
                rka['ins'] = False

            # Include the end.
            if rc.endswith('I') == True:
                rka['ine'] = True

            if 'dly' in rc:

                rka['td'] = datetime.timedelta(days = 1)
                expanded, count = self._rsmp(**rka)

                # Add the list of expanded parameters to the new
                # parameters list.
                expanded_params.extend(expanded)

                # Set the count of expanded parameters in the original
                # params list.
                param['count'] = count

            else:

                # If a resampling method is not defined, then add the
                # "un-expanded" param dictionary to the new list.  Set
                # the count of expanded params to 1.
                expanded_params.append(param)
                param['count'] = 1

        # Call the parent method.
        _data = super(Command, self).handle(
            **{'db': kwargs['db'], 'params': expanded_params})

        # Count the original number of params.
        #cp = 0

        # Increment this counter based upon the count argument added to
        # the original params dictionaries.
        cd = 0

        for param in kwargs['params']:

            # Create a list of data that, at the end of this loop, will
            # be added to the output list.
            _tmp = []

            # Iterate over the parent method's data output based upon
            # the number of date and time intervals used for resampling.
            for i in range(cd, cd + param['count']):

                # Get a single date and time interval parameter from the
                # expanded list of params.
                ep = expanded_params[i]

                # Loop over the returned values for the expanded params.
                for j in _data[i]:

                    _date = j[0]

                    if _date == None:

                        _date = ep['sdate']

                        if str(param.get('rsmp', '')).startswith('-'):

                            _date = ep['edate']

                            if str(param.get('rsmp', '')).endswith('X'):
                                _date += datetime.timedelta(seconds = 1)

                        elif str(param.get('rsmp', '')).startswith('X'):
                            _date -= datetime.timedelta(seconds = 1)

                        _date = _date.strftime('%Y-%m-%dT%H:%M:%S')

                    # Add to the current data list.
                    _tmp.append([_date, j[1]])

            # Add the list of data to the output list.
            data.append(_tmp)

            #cp += 1
            cd += param['count']

        return data

    @staticmethod
    def gen_query(pid, rpt, elm, sdate, edate, **kwargs):

        query = {'reduce': 'false'}

        # Create the start and end key "arrays" for the query,
        # populating the first three elements with the platform ID,
        # report and data element IDs.
        query['startkey'] = [pid, rpt, elm]
        query['endkey'] = [pid, rpt, elm]

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

        # If the reduction flag is not set in the keyword arguments,
        # then specify that the reduce option is false.
        if kwargs.get('reduce', False) == True:
            query['reduce'] = 'true'

        return query

