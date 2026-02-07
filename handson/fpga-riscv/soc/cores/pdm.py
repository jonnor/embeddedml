
"""
PDM microphone input support

Generates clock
"""

from migen import *
from litex.soc.interconnect.csr import *
from litex.soc.interconnect.csr_eventmanager import *

import os.path
here = os.path.dirname(__file__)

class PDMMic(Module, AutoCSR):
    def __init__(self, platform, pads):
        """
        pads should have:
            pads.clk  - PDM clock output
            pads.data - PDM data input
        """
        # CSR registers
        self.enable = CSRStorage(1, description="Enable PDM microphone")
        self.period = CSRStorage(8, reset=4, description="PDM clock period divider")
        self.sample = CSRStatus(16, description="Latest PCM sample")
        
        # Event manager for interrupts
        self.submodules.ev = EventManager()
        self.ev.sample_ready = EventSourceLevel()
        self.ev.finalize()
        
        # Internal signals
        pcm_sample = Signal(16)
        pdm_clk_out = Signal()
        
        # Connect PDM clock output
        self.comb += pads.clk.eq(pdm_clk_out)
        
        # Add Verilog sources
        platform.add_source(os.path.join(here, "pdm_mic.v"))
        platform.add_source(os.path.join(here, "cic3_pdm.v"))
        
        # Instantiate Verilog module
        self.specials += Instance("pdm_mic",
            i_clk=ClockSignal(),
            i_rst=ResetSignal(),
            i_enable=self.enable.storage,
            i_period=self.period.storage,
            i_irq_clear=self.ev.sample_ready.clear,
            i_pdm_data_in=pads.data,
            o_pdm_clk_out=pdm_clk_out,
            o_pcm_sample=pcm_sample,
            o_irq=self.ev.sample_ready.trigger
        )
        
        # Update sample register
        self.sync += self.sample.status.eq(pcm_sample)
