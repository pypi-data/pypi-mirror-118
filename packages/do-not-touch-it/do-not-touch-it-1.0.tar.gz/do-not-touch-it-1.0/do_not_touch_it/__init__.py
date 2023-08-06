class ImmutableMeta(type):
    @classmethod
    def change_init(mcs, method):
        def new_init(self, *args, **kwargs):
            if callable(method):
                method(self, *args, **kwargs)
            object.__setattr__(self, 'locked', True)

        return new_init

    @classmethod
    def change_methods(mcs, method, parent_class, method_name):
        def new_method(self, *args, **kwargs):
            if hasattr(self, 'locked') and self.locked:
                raise TypeError('this object is immutable')
            if callable(method):
                method(self, *args, **kwargs)
            else:
                getattr(parent_class, method_name)(self, *args, **kwargs)
        return new_method

    def __new__(mcs, name, parents, kwargs):
        for i in '__setattr__', '__setitem__', '__delattr__', '__delitem__':
            parent_index = kwargs.get(f'{i[:-1]}index__') or 0
            try:
                parent = parents[parent_index]
            except IndexError:
                parent = object
            kwargs[i] = mcs.change_methods(kwargs.get(i), parent, i)
        kwargs['__init__'] = mcs.change_init(kwargs.get('__init__'))
        return type.__new__(mcs, name, parents, kwargs)


class Immutable(metaclass=ImmutableMeta):
    pass
