# todo : license

import bpy


class PropertyMeta(type):
    def __init__(cls, name, bases, attrs):
        print('init attrs', attrs)
        prop_dict = attrs.get('prop_dict', None)
        assert prop_dict is not None

        # key value pair in prop_dict defines the properties for bpy.type.PropertyGroup sub classes
        # key is the name of the property
        # value is a dict like this:
        # {'name': 'scale',
        #  'type': 'int',
        #  'description': 'blabla' (optional)
        #  'default': '
        #
        for key, value in prop_dict.items():
            attrs[key] = None


