# -*- coding: utf-8 -*-
from case_convert import (
    camel_case,
    kebab_case,
    pascal_case,
    snake_case,
    upper_case
)

case_style_mapping = {
    'camel': camel_case,
    'kebab': kebab_case,
    'snake': snake_case,
    'pascal': pascal_case,
    'upper': upper_case,
}


def case_to_case(case_str, case_style):
    return case_style_mapping[case_style](case_str)
