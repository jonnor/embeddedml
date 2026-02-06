
"""
Simple single-pad Pulse Width Modulation

From 
https://github.com/riktw/LitexTang9KExperiments/blob/main/pwm_core.py
"""

from migen import *

from litex.soc.interconnect.csr import *
from litex.gen import *

class PwmModule(LiteXModule):
    def __init__(self, pad, clock_domain="sys"):
        
        self.enable = CSRStorage(size=1, reset=0, description="Enable the PWM peripheral")
        self.divider = CSRStorage(size=16, reset=0, description="Clock divider")
        self.maxCount = CSRStorage(size=16, reset=0, description="Max count for the PWM counter")
        self.dutycycle = CSRStorage(size=16, reset=0, description="IO dutycycle value")
        
        divcounter = Signal(16, reset=0)
        pwmcounter = Signal(16, reset=0)
        
        sync = getattr(self.sync, clock_domain)
        
        sync += [
            If(self.enable.storage,
                divcounter.eq(divcounter + 1),
                    If(divcounter >= self.divider.storage,
                        divcounter.eq(0),
                        pwmcounter.eq(pwmcounter + 1),
                        If(pwmcounter >= self.maxCount.storage,
                            pwmcounter.eq(0),
                        ),
                    )
                )
            ]
                    
        sync += pad.eq(self.enable.storage & (pwmcounter < self.dutycycle.storage))
        
