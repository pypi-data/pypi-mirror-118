# Standard library imports.
import importlib
from types import ModuleType as _mt

# Local package imports.
from tsofa._views._dbse_prd import Command as _PRD


# Define the data function for retrieving report objects using the
# platform and report ID values.
def _data_prd(resolution, db, params):

    data = None

    if resolution == 'sec':

        _m = importlib.import_module('tsofa._views._dsec_prd')
        data = _m.Command().handle(**{'db': db, 'params': params})

    return data


# Define the data function for retrieving values using the platform,
# report, and element ID values.
def _data_pred(resolution, db, params):

    data = None

    if resolution == 'sec':

        _m = importlib.import_module('tsofa._views._dsec_pred')
        data = _m.Command().handle(**{'db': db, 'params': params})

    return data


# Define a dynamic module for retrieving platform data.
data = _mt('data')
data.prd = _data_prd
data.pred = _data_pred

# Set the summarize method for the "prd" based views.
data.prd.summarize = _PRD.summarize


# Define the function for retrieving platform attribute information
# using the platform and attribute ID values.
def _pfrm_pad(resolution, db, params):

    attrs = None

    if resolution == 'sec':

        _m = importlib.import_module('tsofa._views._psec_pad')
        attrs = _m.Command().handle(**{'db': db, 'params': params})

    return attrs


# Define a dynamic module for retrieving platform attribute information.
pfrm = _mt('pfrm')
pfrm.pad = _pfrm_pad

