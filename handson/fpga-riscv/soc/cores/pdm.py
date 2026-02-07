
"""
PDM microphone input support

Generates clock
"""

from migen import *
from litex.soc.interconnect.csr import *
from litex.soc.interconnect.csr_eventmanager import *
from litex.soc.interconnect import stream
from migen.genlib.cdc import MultiReg

import os.path
here = os.path.dirname(__file__)


class PDMMic(Module, AutoCSR):
    def __init__(self, platform, pads, sys_clk_freq, fifo_depth=256):
        """
        PDM Microphone module with FIFO buffering and 1MHz clock
        
        Args:
            platform: LiteX platform
            pads: PDM pads (clk, data)
            sys_clk_freq: System clock frequency in Hz
            fifo_depth: FIFO depth (default 256)
        """
        # CSR registers
        self.enable = CSRStorage(1, description="Enable PDM microphone")
        self.period = CSRStorage(8, reset=4, description="PDM clock period divider")
        self.fifo_level = CSRStatus(16, description="Current FIFO fill level")
        self.sample = CSRStatus(16, description="Read sample from FIFO")
        
        # Event manager for interrupts
        self.submodules.ev = EventManager()
        self.ev.fifo_threshold = EventSourceLevel()
        self.ev.finalize()
        
        # Generate 1MHz clock enable from system clock
        pdm_clk_freq = 1e6
        clk_div = int(sys_clk_freq / pdm_clk_freq)
        
        pdm_counter = Signal(max=clk_div)
        pdm_clk_en = Signal()
        
        self.sync += [
            If(pdm_counter == (clk_div - 1),
                pdm_counter.eq(0)
            ).Else(
                pdm_counter.eq(pdm_counter + 1)
            )
        ]
        
        self.comb += pdm_clk_en.eq(pdm_counter == 0)
        
        # Create 1MHz clock signal
        pdm_clk_1mhz = Signal()
        pdm_toggle = Signal()
        
        self.sync += [
            If(pdm_clk_en,
                pdm_toggle.eq(~pdm_toggle)
            )
        ]
        
        self.comb += pdm_clk_1mhz.eq(pdm_toggle)
        
        # Internal signals
        pcm_sample_direct = Signal(16)
        pcm_valid = Signal()
        pdm_clk_out = Signal()
        
        # Create FIFO in system clock domain
        self.submodules.fifo = fifo = stream.SyncFIFO(
            [("data", 16)], 
            fifo_depth
        )
        
        # Connect PDM clock output
        self.comb += pads.clk.eq(pdm_clk_out)
        
        # Add Verilog sources
        platform.add_source(os.path.join(here, "pdm_mic.v"))
        platform.add_source(os.path.join(here, "cic3_pdm.v"))
        
        # Instantiate Verilog module with 1MHz clock signal
        self.specials += Instance("pdm_mic",
            i_clk=pdm_clk_1mhz,
            i_rst=ResetSignal(),
            i_enable=self.enable.storage,
            i_period=self.period.storage,
            i_irq_clear=Signal(),  # Not used
            i_pdm_data_in=pads.data,
            o_pdm_clk_out=pdm_clk_out,
            o_pcm_sample=pcm_sample_direct,
            o_pcm_valid=pcm_valid  # Changed from irq
        )
        
        # Clock domain crossing for signals from PDM clock to system clock
        pcm_valid_sys = Signal()
        pcm_sample_sys = Signal(16)
        self.specials += [
            MultiReg(pcm_valid, pcm_valid_sys),
            MultiReg(pcm_sample_direct, pcm_sample_sys)
        ]
        
        # Connect to FIFO (in sys domain) - write when valid
        self.comb += [
            fifo.sink.valid.eq(pcm_valid_sys),
            fifo.sink.data.eq(pcm_sample_sys),
        ]
        
        # Read from FIFO on CSR access
        self.sync += [
            If(self.sample.we,
                If(fifo.source.valid,
                    self.sample.status.eq(fifo.source.data),
                    fifo.source.ready.eq(1)
                ).Else(
                    fifo.source.ready.eq(0)
                )
            ).Else(
                fifo.source.ready.eq(0)
            )
        ]
        
        # FIFO level status
        self.comb += self.fifo_level.status.eq(fifo.level)
        
        # Trigger interrupt when FIFO reaches threshold (half full)
        threshold = fifo_depth // 2
        self.comb += self.ev.fifo_threshold.trigger.eq(fifo.level >= threshold)
