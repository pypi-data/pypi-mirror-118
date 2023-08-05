import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class Attribute:
    Name: str = ''
    Is_class: bool = False
    Is_method: bool = False
