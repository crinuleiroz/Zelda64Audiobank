"""
Helpers
=====
"""
def safe_enum(enum_cls, value: int):
    """
    Safely converts `value` to `enum_cls`

    Args:
        enum_cls (Class): The enum class.
        value (int): The value to convert.
    """
    try:
        return enum_cls(value)
    except ValueError as e:
        raise ValueError(f'Invalid value {value} for enum {enum_cls.__name__}')

def make_property(raw_attr_name, transform):
    def getter(self):
        return transform(getattr(self, f"_{raw_attr_name}_raw"))

    def setter(self, value):
        setattr(self, f'_{raw_attr_name}_raw', value)

    return property(getter, setter)