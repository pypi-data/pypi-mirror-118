from typing import Dict

def to_ordinal(number: int) -> str:
    return f'{number}{get_ordinal_suffix(number)}'

def get_ordinal_suffix(number: int) -> str:
    mapper_dict = {
        1: 'st',
        2: 'nd',
        3: 'rd',
    }
    return (
        'th' if number % 100 in [11, 12, 13]
        else mapper_dict.get(number % 10, 'th')
    )
