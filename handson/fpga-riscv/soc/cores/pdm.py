
"""
PDM microphone input support

Generates clock
"""

from migen import *
from litex.soc.interconnect.csr import *
from litex.soc.interconnect.csr_eventmanager import *
from litex.soc.interconnect import stream

import os.path
here = os.path.dirname(__file__)

class PDMMic(Module, AutoCSR):
    def __init__(self, platform, pads, fifo_depth=128):
        # CSR registers
        self.enable = CSRStorage(1, description="Enable PDM microphone")
        self.period = CSRStorage(8, reset=4, description="PDM clock period divider")
        self.fifo_level = CSRStatus(16, description="Current FIFO fill level")
        self.sample = CSRStatus(16, description="Read sample from FIFO")

        # Event manager
        self.submodules.ev = EventManager()
        self.ev.fifo_threshold = EventSourceLevel()
        self.ev.finalize()
        
        # Internal signals from Verilog
        pcm_sample_direct = Signal(16)
        sample_valid = Signal()
        pdm_clk_out = Signal()
        
        # Create FIFO
        from migen.genlib.fifo import SyncFIFO
        self.submodules.fifo = fifo = SyncFIFO(16, fifo_depth)
        
        # Connect PDM clock
        self.comb += pads.clk.eq(pdm_clk_out)
        
        # Add Verilog sources
        platform.add_source(os.path.join(here, "pdm_mic.v"))
        platform.add_source(os.path.join(here, "cic3_pdm.v"))
        
        # Instantiate your existing Verilog module (unchanged)
        self.specials += Instance("pdm_mic",
            i_clk=ClockSignal(),
            i_rst=ResetSignal(),
            i_enable=self.enable.storage,
            i_period=self.period.storage,
            i_irq_clear=self.ev.fifo_threshold.clear,
            i_pdm_data_in=pads.data,
            o_pdm_clk_out=pdm_clk_out,
            o_pcm_sample=pcm_sample_direct,
            o_irq=sample_valid
        )
        
        # Connect Verilog output to FIFO input
        self.comb += [
            fifo.din.eq(pcm_sample_direct),
            fifo.we.eq(sample_valid & fifo.writable),  # Write when sample valid and FIFO not full
        ]
        
        # Read from FIFO on CSR access
        self.sync += [
            If(self.sample.we,  # When CPU reads the sample register
                If(fifo.readable,
                    self.sample.status.eq(fifo.dout),
                    fifo.re.eq(1)
                )
            ).Else(
                fifo.re.eq(0)
            )
        ]
        
        # FIFO level status
        self.comb += self.fifo_level.status.eq(fifo.level)
        
        # Trigger interrupt when FIFO reaches threshold (e.g., half full)
        threshold = fifo_depth // 2
        self.comb += self.ev.fifo_threshold.trigger.eq(fifo.level >= threshold)
