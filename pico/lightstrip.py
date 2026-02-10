import uasyncio as asyncio
import machine
from asyncio import sleep_ms
import rp2
import time
import array

class LightStrip:

    @rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
    def ws2812():
        T1 = 2
        T2 = 5
        T3 = 3
        wrap_target() # type: ignore
        label("bitloop") # type: ignore
        out(x, 1)               .side(0)    [T3 - 1] # type: ignore
        jmp(not_x, "do_zero")   .side(1)    [T1 - 1] # type: ignore
        jmp("bitloop")          .side(1)    [T2 - 1] # type: ignore
        label("do_zero") # type: ignore
        nop()                   .side(0)    [T2 - 1] # type: ignore
        wrap() # type: ignore

    def __init__(self, sm_id: int, pin: machine.Pin, leds: int, debug=False):
        self.leds = leds
        # Create the StateMachine with the ws2812 program, outputting on pin
        self.sm = rp2.StateMachine(sm_id, self.ws2812, freq=8_000_000, sideset_base=pin)
        self.sm.active(1)
        self.ar = array.array("I", [0 for _ in range(leds)])
        self._debug = debug

    def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.leds)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF))
            g = int(((c >> 16) & 0xFF))
            b = int((c & 0xFF))
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)
        time.sleep_ms(10)

    def pixels_set(self,i,color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

    @property
    def debug(self):
        return self._debug

class Color:

    BLACK = [0,0,0]
    OFF = [0,0,0]

    def __init__(self, hex_color):
        c = tuple(int(hex_color[i:i+2], 16)  for i in (1, 3, 5))
        self._r = c[0]
        self._g = c[1]
        self._b = c[2]

    @property
    def r(self):
        return self._r
    
    @property
    def g(self):
        return self._g
    
    @property
    def b(self):
        return self._b
    
    @property
    def rgb(self):
        return [self._r,self._g,self._b]
    
    def rgb_b(self, brightness = 1):
        return [int(self._r * brightness), int(self._g * brightness), int(self._b * brightness)]

class Led:

    def __init__(self, id: int):
        self._id = id
    
    @property
    def id(self) -> int:
        return self._id

class ColoredLed(Led):

    def __init__(self, id, color:Color):
        Led.__init__(self, id)
        self._color = color
    
    @property 
    def color(self) -> Color: 
        return self._color



class Action:
    async def run(self, l: LightStrip):
        pass

class WaitAction(Action):

    def __init__(self, dur_ms: int = 0):
        self._dur_ms = dur_ms
        
    async def run(self, l: LightStrip):
        await sleep_ms(self._dur_ms)
        
class SwitchOnAction(Action):

    def __init__(self, led_group: list[ColoredLed]):
        self._led_group = led_group
        
    async def run(self, l: LightStrip):
        for led in self._led_group:
            # print(f"Switching led {led.id} ON.. ")
            l.pixels_set(led.id, led.color.rgb)
        l.pixels_show()
   
class SwitchOffAction(Action):

    def __init__(self, led_group: list):
        self._led_group = led_group
        
    async def run(self, l: LightStrip):
        for led in self._led_group:
            # print(f"Switching led {led.id} OFF.. ")
            l.pixels_set(led.id, Color.OFF)
        l.pixels_show()

class SwitchOnOffAction(Action):

    def __init__(self, led_group: list[ColoredLed], dur_ms: int):
        self._led_group = led_group
        self._dur_ms = dur_ms
        
    async def run(self, l: LightStrip):
        for led in self._led_group:
            l.pixels_set(led.id, led.color.rgb)
        l.pixels_show()
        await sleep_ms(self._dur_ms)
        for led in self._led_group:
            l.pixels_set(led.id, Color.OFF)
        l.pixels_show()

class DimInOutAction(Action):

    def __init__(self, led_group: list[ColoredLed], dur_ms: int, factor: float = 1.2):
        self._led_group = led_group
        self._dur_ms = dur_ms
        self.curve_values = list()        
        brightness = 1
        self.curve_values.append(0)
        while brightness < 100:
            brightness = brightness * factor
            self.curve_values.append(brightness/100)
        self.curve_values.append(1)
        
    async def run(self, l: LightStrip):   
        
        dur_dim = 0
        for brightness in self.curve_values:
            for led in self._led_group:
                l.pixels_set(led.id, (int(led.color.r * (brightness)),int(led.color.g * (brightness)),int(led.color.b * (brightness))))
            l.pixels_show()
            await sleep_ms(2)
            dur_dim = dur_dim + 2
        
        if dur_dim > 0:
            await sleep_ms(self._dur_ms - (dur_dim*2))

        for brightness in self.curve_values[::-1]:
            for led in self._led_group:
                l.pixels_set(led.id, (int(led.color.r * (brightness)),int(led.color.g * (brightness)),int(led.color.b * (brightness))))
            l.pixels_show()
            await sleep_ms(2)

class DimInAction(Action):

    def __init__(self, led_group: list[ColoredLed], factor: float = 1.2):
        self._led_group = led_group
        self.curve_values = list()        
        brightness = 1
        self.curve_values.append(0)
        while brightness < 100:
            brightness = brightness * factor
            self.curve_values.append(brightness/100)
        self.curve_values.append(1)
        
    async def run(self, l: LightStrip):   
        for brightness in self.curve_values:
            for led in self._led_group:
                l.pixels_set(led.id, (int(led.color.r * (brightness)),int(led.color.g * (brightness)),int(led.color.b * (brightness))))
            l.pixels_show()
            await sleep_ms(2)

class DimOutAction(Action):

    def __init__(self, led_group: list[ColoredLed], factor: float = 1.2):
        self._led_group = led_group
        self.curve_values = list()        
        brightness = 1
        self.curve_values.append(0)
        while brightness < 100:
            brightness = brightness * factor
            self.curve_values.append(brightness/100)
        self.curve_values.append(1)
        
    async def run(self, l: LightStrip):   
        for brightness in self.curve_values[::-1]:
            for led in self._led_group:
                l.pixels_set(led.id, (int(led.color.r * (brightness)),int(led.color.g * (brightness)),int(led.color.b * (brightness))))
            l.pixels_show()
            await sleep_ms(2)

class Effect:

    task: asyncio.Task = None

    def start(self, l: LightStrip):
        self.task = asyncio.create_task(self.execute(l))

    def stop(self):
        if not (self.task is None):
            self.task.cancel()
            self.task = None
    
    def is_running(self): 
        return not (self.task is None)
    
    async def execute(self, l: LightStrip):
        pass

class SimpleEffect(Effect):

    debug: bool

    def __init__(self, label, start_actions: list, stop_actions: list):        
        self.start_actions = start_actions
        self.stop_actions = stop_actions
        self.label = label
            
    async def execute(self, l: LightStrip):
        print(f"FX ({self.label}) started... ")
        try:
            for action in self.start_actions:
                await action.run(l)
            while True:
                await sleep_ms(1000)
        except: 
            pass
        finally:
            for action in self.stop_actions:
                await action.run(l)
            print(f"... FX ({self.label}) finished")

class LoopEffect(SimpleEffect):    
    
    def __init__(self, label, start_actions: list, stop_actions: list):        
        self.start_actions = start_actions
        self.stop_actions = stop_actions
        self.label = label

    async def execute(self, l: LightStrip):
        print(f"FX ({self.label}) started... ")
        try:    
            while True:
                for action in self.start_actions:
                    await action.run(l)
        except: 
            pass
        finally:
            for action in self.stop_actions:
                await action.run(l)
            print(f"... FX ({self.label}) finished")