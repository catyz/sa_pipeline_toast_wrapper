"""
Akito Kusaka, June 17th, 2020.
Based on the code by John Groh, October 2018
"""

import numpy as np
# from .sa_globals import log_error, log_warn, log_info
# from toast import qarray as qa

class TodBase:
    """
    Copied from sa_tod.TOD.
    This class implements aspects common to both non-toast and toast based TOD object.
    Currently, the implementation overrides read_... functions.
    But I presume one can override _get_... functions instead?
    I am unsure how to use these to methods differently.
    """
    def __init__(self):
        self._source_prefix = '' # Only used for toast based

    def set_source_prefix(self,prefix):
        self._source_prefix = prefix
        
    def read(self, source):
        """
        Return samples for whatever stream you specify
        Could be a detector, the HWP angle, fridge temperatures, etc.
        Arguments:
        ----------
        source : string
            name of data source to access
        """
        _source = self._source_prefix+source
        return self.cache[_source]

    def write(self, source, values, quiet=False):
        """
        Add another stream to the TOD with name 'source' and values 'values'
        Allow for overwriting
        """
        _source = self._source_prefix+source
        if _source in self.cache.keys() and not quiet:
            print('WARNING: Overwriting field name {:s} in TOD'.format(_source), file=log_warn)
        self.cache[_source] = values

    def delete(self, source):
        """
        Delete the stream with name 'source' to save memory
        """
        _source = self._source_prefix+source
        assert _source in self.cache.keys()
        del self.cache[_source]
        
    def read_common_flags(self):
        # Will we use these?
        raise NotImplementedError

    def read_flags(self, detector=None):
        # Incorporate common flags here?
        raise NotImplementedError

    def read_boresight(self):
        """
        return the boresight pointing in equatorial coordinates, represented by quaternions
        """
        return self.read('boresight')

    def read_boresight_azel(self):
        """
        return the boresight pointing in telescope coordinates, represented by quaternions
        """
        return self.read('boresight_azel')

    def read_times(self):
        "Return the bolometer timestamps"
        return self.read('bolo_time')


class TodNoToast(TodBase):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache

class TodNoToastWrapper:
    # Function to be added: way to concatenate two 'tod_list'
    
    def __init__(self, tod_list):
        self.tod_list = tod_list
        self._current_tod_index = 0
        self._input_name_list = [t.read('input_name') for t in self.tod_list]

    def set_tod_index(self, tod_index):
        # I don't like this.  Really, one should not use state of an object this way.  Oh, well.
        # Obviously, this makes things thread unsafe.
        self._current_tod_index = tod_index

    def get_tod_index(self):
        return self._current_tod_index
        
    def get_input_name_list(self):
        return self._input_name_list

    def __getattr__(self, method):
        return getattr(self.tod_list[self._current_tod_index],method)

    def __getitem__(self, idx):
        return self.tod_list[idx]

    def __add__(self, rhs):
        n_tod = len(self._input_name_list) + len(rhs._input_name_list)
        assert len(set(self._input_name_list + rhs._input_name_list)) == n_tod
        return TodNoToastWrapper(self.tod_list + rhs.tod_list)
