
from ...Base import *

from typing import Union, Optional, List, Tuple

class HasTemp:
    pass
        
# '.dc srcnam vstart vstop vincr [src2 start2 stop2 incr2]'

# class DC(SpiceElement):
#     def __init__(
#         self,
#         src_name: 
#     ) -> None:
#         super().__init__(comp_prefix='dc')
#         self.id.etype = SpiceElementType.ANALYSIS
#         self.src_name = src_name