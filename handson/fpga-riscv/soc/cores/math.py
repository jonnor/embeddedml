
from migen import *
from litex.soc.interconnect.csr import *

class SIMD_PADD8_Signed(Module, AutoCSR):
    def __init__(self):
        self.op_a = CSRStorage(32, description="Operand A (4x8-bit signed)")
        self.op_b = CSRStorage(32, description="Operand B (4x8-bit signed)")
        self.result = CSRStatus(32, description="Result (4x8-bit signed)")
        
        # # #
        
        # Split into lanes
        a_lanes = [Signal((8, True)) for _ in range(4)]  # True = signed
        b_lanes = [Signal((8, True)) for _ in range(4)]
        result_lanes = [Signal((8, True)) for _ in range(4)]
        
        for i in range(4):
            self.comb += [
                a_lanes[i].eq(self.op_a.storage[i*8:(i+1)*8]),
                b_lanes[i].eq(self.op_b.storage[i*8:(i+1)*8]),
                result_lanes[i].eq(a_lanes[i] + b_lanes[i])  # Signed add
            ]
        
        self.comb += self.result.status.eq(Cat(*result_lanes))
