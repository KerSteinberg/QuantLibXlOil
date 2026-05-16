# we use quantlibpy.py to avoid confusion with the quantlib module in the same package.

import QuantLib as ql
import xloil as xlo

from .config import EXCEL_GROUP_NAME, TRIGGER_ARG, TRIGGER_DESC

@xlo.func(
    help='Return the QuantLib version as a string',
    args={TRIGGER_ARG : TRIGGER_DESC},
    group=EXCEL_GROUP_NAME,
)
def qlVersion(trigger = None):
    return ql.__version__


@xlo.func(
    help='Return the QuantLib hex version as an integer',
    args={TRIGGER_ARG : TRIGGER_DESC},
    group=EXCEL_GROUP_NAME,
)
def qlHexVersion(trigger = None):
    return ql.__hexversion__
