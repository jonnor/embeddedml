
"""
Simple custom peripheral/core for testing handling of interrupts in C
"""

from migen import *
from litex.soc.interconnect.csr import *
from litex.soc.interconnect.csr_eventmanager import EventManager, EventSourceLevel

import os.path
here = os.path.dirname(__file__)


class TimerIRQ(Module, AutoCSR):
    def __init__(self, platform):
        self.platform = platform

        self.prescaler = CSRStorage(32, reset=0)
        self.count = CSRStorage(32, reset=0)
        self.enable = CSRStorage(1)
        
        # EventManager for interrupt
        self.submodules.ev = EventManager()
        self.ev.timer = EventSourceLevel()
        self.ev.finalize()

        # Intermediate signal from Verilog
        irq_out = Signal()

        # Add Verilog source
        self.platform.add_source(os.path.join(here, "timer_irq.v"))

        # Instantiate Verilog module
        self.specials += Instance("timer_irq",
            i_clk=ClockSignal(),
            i_rst=ResetSignal(),
            i_prescaler=self.prescaler.storage,
            i_count=self.count.storage,
            i_enable=self.enable.storage,
            i_irq_clear=self.ev.timer.clear,
            o_irq=irq_out
        )
        
        # Connect to EventManager
        self.comb += self.ev.timer.trigger.eq(irq_out)
