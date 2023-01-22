from enum import Enum
from typing import Union

import QuantLib as ql


class OptionTypeEnum(Enum):
    CALL = 'call'
    PUT = 'put'

    @staticmethod
    def values():
        return [e.value for e in OptionTypeEnum]


def convert_option_type_to_ql(option_type: Union[str, OptionTypeEnum]):
    if isinstance(option_type, str):
        option_type = option_type.upper()
        if option_type not in OptionTypeEnum.__members__:
            raise ValueError(f"Invalid option type, expected one of {list(OptionTypeEnum.__members__.keys())}")
        return convert_option_type_to_ql(OptionTypeEnum[option_type])
    elif isinstance(option_type, OptionTypeEnum):
        if option_type == OptionTypeEnum.CALL:
            return ql.Option.Call
        elif option_type == OptionTypeEnum.PUT:
            return ql.Option.Put
        else:
            raise ValueError(f"Invalid option type: {option_type}")
    else:
        raise
