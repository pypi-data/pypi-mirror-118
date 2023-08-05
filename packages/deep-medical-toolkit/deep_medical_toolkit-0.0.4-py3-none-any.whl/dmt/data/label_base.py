
import logging
import weakref

class Label(dict):
    """ Base class for all labels (e.g. masks, class ids). """
    
    # Class Variables
    _id_counter = 0  # global runtime ID generator for all Image subclasses
    _gid_to_instance = weakref.WeakValueDictionary()
    _reserved_attributes = ['num_classes', 'class_names']
    
    def __init__(self, **kwargs):
        
        # Global Label class ID tracking
        self.gid = Label._id_counter
        Label._gid_to_instance[self.gid] = self  # save memory
        Label._id_counter += 1
        
        super().__init__(**kwargs)  # update given attributes to dict
        self.update_attributes()  # make dot notation available
    
    @property
    def num_classes(self):
        raise NotImplementedError()  # weak enforcement
    
    @property
    def class_names(self):
        raise NotImplementedError()  # weak enforcement
    
    def get_one_hot(self):
        raise NotImplementedError()  # weak enforcement
    
    def get_ids(self):
        raise NotImplementedError()  # weak enforcement
    
    ### Functions below offers compatible/correct dict functionality
    ###   e.g. must update __dict__ after every update & override default funcs
    
    def __setattr__(self, name, value):
        """ Setting attrs in dot notation requires updating dict. """
        name = self._parse_new_attribute(name)
        self[name] = value
        super().__setattr__(name, value)
    
    def __getitem__(self, item):
        item = super().__getitem__(item)
        gid = None if not hasattr(self, 'gid') else self.gid
        logging.debug(f'Sample {gid}: Getting item: {item}')
        return item
    
    def __setitem__(self, key, value):
        key = self._parse_new_attribute(key)
        super().__setitem__(key, value)
        self.update_attributes()
        gid = None if not hasattr(self, 'gid') else self.gid
        logging.debug(f'Sample {gid}: Getting item: {value}')
        
    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                msg = f"Update expected at most 1 arguments, got {len(args)}."
                raise TypeError(msg)
            for k, v in dict(args[0]).items():
                k = self._parse_new_attribute(k)
                self[k] = v
        for k, v in kwargs.items():
            k = self._parse_new_attribute(k)
            self[k] = v
        self.update_attributes()
            
    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        self.update_attributes()
        return self[key]
    
    def update_attributes(self):
        # Allows attribute access through dot notation, e.g. image.spacing
        self.__dict__.update(self)
        
    def _parse_new_attribute(self, attribute):
        return attribute
        
        # TODO gatekeep user attribute setting
        msg = (f'Given attribute "{attribute}" is a reserved attribute '
               f'for class {type(self).__name__}.')
        assert attribute not in self._reserved_attributes, msg
        
        msg = f'Given attribute "{attribute}" cannot start with "_".'
        assert attribute[0] != '_', msg
        
        return attribute
    
    

    
