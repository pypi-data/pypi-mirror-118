from dataclasses import dataclass

@dataclass
class Property:
    Name: str = ''
    Code: str = ''
    Access_modifiers: str = ''
    Is_static: bool = False
    Return_type: str = ''
    Has_get: bool = False
    Has_set: bool = False
    Return_value: str = 'false'
