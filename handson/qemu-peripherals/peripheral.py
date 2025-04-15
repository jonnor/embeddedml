import gdb

class PeripheralEmulator:
    def __init__(self):
        self.peripheral_base = 0x40010000
        self.peripheral_size = 0x1000
        self.registers = {}
        
        # Initialize some example registers with default values
        self.registers[0x100] = 0  # Counter register
        self.registers[0x104] = 0xA5  # Status register
        
        # Set up watchpoints for the entire peripheral region
        self.setup_watchpoints()
        
        print("Peripheral emulator initialized")
        
    def setup_watchpoints(self):
        # Create read watchpoints for our peripheral registers
        gdb.execute(f"watch *(unsigned *)0x{self.peripheral_base + 0x100:08x}")
        gdb.execute(f"watch *(unsigned *)0x{self.peripheral_base + 0x104:08x}")
        
        # Register our watchpoint handler
        gdb.events.stop.connect(self.handle_watchpoint)
        print('setup watchpoints done')

    def handle_watchpoint(self, event):
        if isinstance(event, gdb.BreakpointEvent):
            wp = event.breakpoint
            if wp.type == gdb.BP_WATCHPOINT:
                addr = int(wp.location.split('*')[1], 0)
                offset = addr - self.peripheral_base
                
                # Is this address in our peripheral range?
                if offset >= 0 and offset < self.peripheral_size:
                    print(f"Access to peripheral at offset 0x{offset:x}")
                    
                    # Handle specific registers
                    if offset == 0x100:  # Counter register
                        self.registers[offset] += 1
                        value = self.registers[offset]
                        print(f"Counter incremented to {value}")
                    elif offset == 0x104:  # Status register
                        self.registers[offset] = 0xA5 if self.registers[offset] == 0x5A else 0x5A
                        value = self.registers[offset]
                        print(f"Status toggled to 0x{value:x}")
                    else:
                        value = self.registers.get(offset, 0)
                    
                    # Set the value to be returned by the read
                    gdb.execute(f"set *(unsigned *)0x{addr:x} = 0x{value:x}")
                    
                    # Continue execution
                    gdb.execute("continue")

# Initialize our peripheral emulator when this script is loaded
peripheral = PeripheralEmulator()

# Define a convenience command to inspect peripheral state
class InspectPeripheralCommand(gdb.Command):
    def __init__(self):
        super().__init__("inspect-peripheral", gdb.COMMAND_USER)
    
    def invoke(self, arg, from_tty):
        for offset, value in peripheral.registers.items():
            print(f"Register 0x{offset:x}: 0x{value:x}")

InspectPeripheralCommand()
