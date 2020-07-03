import sa_tod

class FakeToastTod(object):
    # I just generate this as toast.TOD.  replace it with toast.TOD
    def __init__(self, mpicomm=None, detectors=None, samples=None, detindx=None, detranks=None):
        self.cache = {} # toast.TOD holds data container.
        
    def read(self,source):
        return '"read": see if this function is being called.'

    def func_only_in_toast(self):
        return 'func_only_in_toast: see if this function is being called.'

class TodToastWrapper(sa_tod.TodBase,FakeToastTod):
    def __init__(self,
                 tod_list=None,
                 input_name_list=None, tod_cache=None): # Need to rewrite the way to instantiate the class.
        sa_tod.TodBase.__init__(self)
        FakeToastTod.__init__(self) # If you want to pass arguments for TOAST here, you can do so here following the self argument.

        self._current_tod_index = 0
        
        if tod_list is not None:
            assert input_name_list is None  and  tod_cache is None
            
            self._input_name_list = [t.read('input_name') for t in tod_list]
            
            # Substitute the cache content.
            for tod,input_name in zip(tod_list,self._input_name_list):
                for key,value in tod.cache.items():
                    self.cache[input_name+'_'+key] = value
        else:
            assert input_name_list is not None  and  tod_cache is not None

            self._input_name_list = input_name_list
            for key,value in tod_cache.items():
                self.cache[key] = value

    @classmethod
    def from_tod_cache(cls, input_name_list, tod_cache):
        return cls(input_name_list=input_name_list, tod_cache=tod_cache)
        
    def set_tod_index(self, tod_index):
        # I don't like this.  Really, one should not use state of an object this way.  Oh, well.
        # Obviously, this makes things thread unsafe.
        self._current_tod_index = tod_index
        self.set_source_prefix(self._input_name_list[self._current_tod_index]+'_')

    def get_tod_index(self):
        return self._current_tod_index

    def get_input_name_list(self):
        return self._input_name_list

    def __getitem__(self, idx):
        class _TodSingle:
            def __init__(self, tod, tod_index):
                self._tod_index = tod_index
                self._tod = tod

            def set_tod_index(self, tod_index):
                raise RuntimeError('_TodSingle.set_tod_index(...): this should not be called.')

            def get_input_name_list(self):
                raise RuntimeError('_TodSingle.get_input_name_list(): this should not be called.')
            
            def __getattr__(self, method):
                # Prepare method wrapper in case function name is used as a handler.
                # Again, this isn't really thread safe.
                def method_wrapper(*args,**argv):
                    tod_idx_before = self._tod.get_tod_index()
                    try:
                        self._tod.set_tod_index(self._tod_index)
                        return getattr(self._tod,method)(*args,**argv)
                    finally:
                        # This part called after returning.
                        self._tod.set_tod_index(tod_idx_before)
                        
                return method_wrapper
            
        return _TodSingle(self, idx)
    
    def __add__(self, rhs):
        input_name_list = self._input_name_list + rhs._input_name_list
        assert len(set(input_name_list)) == len(input_name_list)
        tod_cache = dict(**self.cache, **rhs.cache)
        return self.from_tod_cache(input_name_list, tod_cache)
