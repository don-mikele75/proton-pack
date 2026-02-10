
from machine import Pin
from asyncio import sleep

class Switch:

    state = False
    
    def __init__(self, switch, label, debug=False):
        self.switch = switch
        self.label = label
        self.listeners = list()
        self.state = False
        self.debug = debug
        
    def add_listener(self, func):
        self.listeners.append(func)
        
    async def run_watchdog(self):        
        while True:
                
            if (self.switch.value() == 1) and (self.state == False):
                self.state = True
                for func in self.listeners:
                    print(f"+++ Switch {self.label} turned ON")
                    await func(self.state)
                
                
            if (self.switch.value() == 0) and (self.state == True):
                self.state = False
                for func in self.listeners:
                    print(f"--- Switch {self.label} turned OFF")
                    await func(self.state)

            await sleep(0.1)