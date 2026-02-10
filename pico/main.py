import uasyncio as asyncio
import fx
from machine import Pin,soft_reset
from switch import Switch
from player import Player
from lightstrip import LightStrip

DEBUG = False
OFFLINE = 0
ONLINE = 1
power_state = OFFLINE

# =============== HW init
# =============== Pins Buttons 22 (white),26 (yellow),27 (blue) ,28 (green)
player = Player(Pin(0),Pin(1),Pin(2),0,DEBUG)

thrower = LightStrip(1, Pin(6),19,DEBUG) # yellow wire
pack = LightStrip(2, Pin(9),56,DEBUG) # green wire

power_switch = Switch(Pin(26, mode=Pin.IN), "*POWER*",DEBUG)
fire_switch = Switch(Pin(22, Pin.IN), "*FIRE*",DEBUG)
soundtrack_switch = Switch(Pin(28, Pin.IN), "*SOUNDTRACK*",DEBUG)
test_switch = Switch(Pin(27, Pin.IN), "*TEST*",True)


# =============== Button (Test)
async def handle_test_switch(state):
    if state:
        fx.stroke_effect_pack.start(pack)
        fx.stroke_effect_thrower.start(thrower)
    else:
        fx.stroke_effect_pack.stop()
        fx.stroke_effect_thrower.stop()

# =============== Button (Res.)
async def handle_soundtrack_switch(state):
    if state:
        fx.soundtrack_effect_pack1.start(pack)
        fx.soundtrack_effect_pack2.start(pack)
        player.start("gb-soundtrack.wav", continuous=True)
    else:
        fx.soundtrack_effect_pack1.stop()
        fx.soundtrack_effect_pack2.stop()
        player.stop()

# =============== Fire Button
override_task: asyncio.Task = None

async def fire_finished():
    fx.fire_effect.stop()
    if not (override_task is None):
        override_task.cancel()
    if fx.fire_override_effect.is_running():
        print("... override stopped...")
        fx.fire_override_effect.stop()
        fx.ring_override_effect.stop()
        fx.pack_segment_override_effect.stop()
        print("... back to standard")
        fx.ring_effect.start(pack)
        fx.pack_segment_effect.start(pack)

async def handle_fire_switch(state):
    global power_state, override_task
    if power_state == ONLINE:
        if state:
            fx.fire_effect.start(thrower)
            player.start("gb-fire.wav", fire_finished)
            override_task = asyncio.create_task(wait_for_override())
        else:
            player.stop()
            await fire_finished()

async def wait_for_override():
    await asyncio.sleep_ms(5000)
    if (fx.fire_effect.is_running):
        print("... OVERRIDE !!!...")
        fx.pack_segment_effect.stop()
        fx.pack_segment_override_effect.start(pack)
        fx.ring_effect.stop()
        fx.ring_override_effect.start(pack)
        fx.fire_effect.stop()
        fx.fire_override_effect.start(thrower)

# =============== Power Switch
async def warmup_finished():
    global power_state
    fx.led_white_effect.start(thrower)
    power_state = ONLINE

async def shutdown_finished():
    global led_red_task,led_white_task
    fx.led_red_effect.stop()
    fx.led_white_effect.stop()

async def handle_power_switch(state):
    global play_startup_task,play_fire_task,power_state
    if state:
        player.start("gb-startup.wav", warmup_finished)
        fx.led_red_effect.start(thrower)
        fx.blue_yello_toggle_effect.start(thrower)
        fx.segment_effect.start(thrower)
        fx.pack_segment_effect.start(pack)
        fx.ring_effect.start(pack)
        fx.tower_effect.start(pack)

    else:
        power_state = OFFLINE
        fx.fire_effect.stop()
        player.stop()
        player.start("gb-shutdown.wav", shutdown_finished)
        fx.blue_yello_toggle_effect.stop()
        fx.segment_effect.stop()
        fx.ring_effect.stop()
        fx.tower_effect.stop()
        fx.pack_segment_effect.stop()

# =============== Main Loop
def handle_exception(loop,context):
    msg = str(context["exception"] if "exception" in context else context["message"])
    print(msg)
    soft_reset()

async def main():
    # await handle_power_switch(True)
    power_switch.add_listener(handle_power_switch)
    fire_switch.add_listener(handle_fire_switch)
    test_switch.add_listener(handle_test_switch)
    soundtrack_switch.add_listener(handle_soundtrack_switch)
    asyncio.create_task(power_switch.run_watchdog())
    asyncio.create_task(fire_switch.run_watchdog())
    asyncio.create_task(soundtrack_switch.run_watchdog())
    asyncio.create_task(test_switch.run_watchdog())
    await asyncio.get_event_loop().run_forever()

print("======== Ghostbusters Proton Pack =========")
print("READY FOR YOUR COMMANDS!")

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)

asyncio.run(main())