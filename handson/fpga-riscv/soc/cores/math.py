from migen import *
from litex.soc.interconnect.csr import *

import os.path
here = os.path.dirname(__file__)


class SIMD_PADD8_Signed(Module, AutoCSR):
    def __init__(self, platform):
        self.op_a = CSRStorage(32, description="Operand A")
        self.op_b = CSRStorage(32, description="Operand B")
        self.result = CSRStatus(32, description="Result")

        # Add Verilog source
        platform.add_source(os.path.join(here, "simd_padd8.v"))
        
        # Instantiate Verilog module
        self.specials += Instance("simd_padd8_signed",
            i_op_a=self.op_a.storage,
            i_op_b=self.op_b.storage,
            o_result=self.result.status
        )
