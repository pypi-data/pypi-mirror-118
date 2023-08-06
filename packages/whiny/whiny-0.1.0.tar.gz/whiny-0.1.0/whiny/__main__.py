import inspect

class _Nothing:
    pass


# Sentinel to differentiate between None type and Nothing type.
_NOTHING = _Nothing()


class Whiny:
    """Simple validation leveraging Python's descriptor protocol."""

    def __init__(self, typ=_NOTHING, default=_NOTHING, validator=None):
        self._typ = typ
        self._default = default
        self._validator = validator
        self._validate_default()

    def __set_name__(self, owner, name):
        """This helps the descriptor to be aware of the name of the attribute
        it was called on."""

        # Separate private and public names are required to avoid recursion error.
        self._private_name = "_" + name
        self._public_name = name

    def __get__(self, instance, owner):
        # If the descriptor attached to the attribute gets called on the class,
        # this conditional helps to avoid attribute error.
        if instance is None:
            if not self._default is _NOTHING:
                return self._default
            return self
        return getattr(instance, self._private_name)

    def __set__(self, instance, value):
        self.validate(self._typ, value, self._validator)
        setattr(instance, self._private_name, value)

    def _validate_default(self):
        """This needs to be separate from 'validate' because __set_name__ is
        called after __init__().

        """
        value = self._default
        typ = self._typ
        validator = self._validator

        if not inspect.isclass(typ):
            raise TypeError('type needs to be a class')


        if value is not _NOTHING:
            if not isinstance(value, typ):
                raise TypeError(f"default value '{value}' is not of type '{typ}'")

            if validator:
                if not callable(validator):
                    raise TypeError("validator must be a callable")

                validator(value)


    def validate(self, typ, value, validator):
        if not isinstance(value, typ):
            raise TypeError(
                f"attribute '{self._public_name}' is not of type '{str(self._typ)}'"
            )

        if validator:
            if not callable(validator):
                raise TypeError(
                    f"validator on attribute '{self._public_name}' must be a callable",
                )
            validator(value)

    def __repr__(self):
        return f"Whiny(typ={self._typ}, default={self._default})"


class Foo:
    a = Whiny(int, 10, validator=lambda x: x)
    b = Whiny(dict, {'dict': 'val'})

    print('validated!')
