from lightstrip import  \
    Led,Color,ColoredLed, \
    WaitAction,SwitchOnAction,SwitchOffAction,SwitchOnOffAction,DimInOutAction,DimInAction,DimOutAction, \
    SimpleEffect,LoopEffect

def create_colored_leds(leds: list[Led], color:Color) ->  list[ColoredLed]:
    l = list()
    for led in leds:
        l.append(ColoredLed(led.id, color))
    return l


led_red_test = ColoredLed(0, Color('#FFFFFF'))
leds_segment_test = create_colored_leds([Led(1),Led(2),Led(3),Led(4),Led(5),Led(6),Led(7),Led(8)], Color('#FFFFFF'))
led_blue_test = ColoredLed(9, Color('#FFFFFF'))
led_yellow_test = ColoredLed(10, Color('#FFFFFF'))
led_white_test = ColoredLed(11, Color('#FFFFFF'))
leds_fire_test = [Led(12),Led(13),Led(14),Led(15),Led(16),Led(17),Led(18)]
led_test_effect = SimpleEffect("Thrower - White LED",
    [ 
        SwitchOnAction([led_red_test]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[0]]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[1]]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[2]]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[3]]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[4]]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[5]]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[6]]),
        WaitAction(800),
        SwitchOnAction([leds_segment_test[7]]),
        WaitAction(800),
        SwitchOnAction([led_blue_test]),
        WaitAction(800),
        SwitchOnAction([led_yellow_test]),
        WaitAction(800),
        SwitchOnAction([led_white_test]),
        WaitAction(800),
        SwitchOnAction(create_colored_leds(leds_fire_test, Color('#FFFFFF'))),
    ],
    [ 
        SwitchOffAction([led_red_test]),
        SwitchOffAction(leds_segment_test),
        SwitchOffAction([led_blue_test]),
        SwitchOffAction([led_yellow_test]),
        SwitchOffAction([led_white_test]),
        SwitchOffAction(leds_fire_test)
    ]
)

led_red = ColoredLed(0, Color('#C80000'))
led_red_effect = SimpleEffect("Thrower - Red LED",
    [ SwitchOnAction([led_red]) ],
    [ SwitchOffAction([led_red]) ]
)

led_white = ColoredLed(11, Color('#C8C8C8'))
led_white_effect = SimpleEffect("Thrower - White LED",
    [ SwitchOnAction([led_white]) ],
    [ SwitchOffAction([led_white]) ]
)

led_blue = ColoredLed(9, Color('#0000C8'))
led_yellow = ColoredLed(10, Color('#C8C800'))
blue_yello_toggle_effect = LoopEffect("Thrower - Toggle Blue and Yello LED",
    [
        SwitchOnOffAction([led_blue], 500),
        SwitchOnOffAction([led_yellow], 500)
    ],
    [
        SwitchOffAction([led_blue]),
        SwitchOffAction([led_yellow])
    ]    
)

leds_fire = [Led(12),Led(13),Led(14),Led(15),Led(16),Led(17),Led(18)]
fire_effect = LoopEffect("Thrower - Fire",
    [
        SwitchOnAction(create_colored_leds(leds_fire, Color('#B200ED'))),
        WaitAction(40),
        SwitchOnAction(create_colored_leds(leds_fire, Color('#FFFFFF'))),
        WaitAction(5),
        SwitchOnAction(create_colored_leds(leds_fire, Color('#C64B8C'))),
        WaitAction(40),
        SwitchOnAction(create_colored_leds(leds_fire, Color('#B660CD'))),
        WaitAction(40),
    ],
    [
        SwitchOffAction(leds_fire)
    ]
)
fire_override_effect = LoopEffect("Thrower - Fire OVERRIDE",
    [
        SwitchOnAction(create_colored_leds(leds_fire, Color("#1B0123"))),
        WaitAction(40),
        SwitchOnAction(create_colored_leds(leds_fire, Color("#171717"))),
        WaitAction(5),
        SwitchOnAction(create_colored_leds(leds_fire, Color("#1B0B14"))),
        WaitAction(40),
        SwitchOnAction(create_colored_leds(leds_fire, Color("#170C1A"))),
        WaitAction(40),
    ],
    [
        SwitchOffAction(leds_fire)
    ]
)

leds_segment = \
    create_colored_leds([Led(6),Led(5)],Color('#960000')) + \
    create_colored_leds([Led(4),Led(3)],Color('#969600')) + \
    create_colored_leds([Led(2)],Color('#009600'))
segment_effect = SimpleEffect("Thrower - Segment",
    [
        SwitchOnAction([leds_segment[0]]), WaitAction(300),
        SwitchOnAction([leds_segment[1]]), WaitAction(300),
        SwitchOnAction([leds_segment[2]]), WaitAction(600),
        SwitchOnAction([leds_segment[3]]), WaitAction(600),
        SwitchOnAction([leds_segment[4]])
    ],
    [
        SwitchOffAction([leds_segment[4]]), WaitAction(100),
        SwitchOffAction([leds_segment[3]]), WaitAction(150),
        SwitchOffAction([leds_segment[2]]), WaitAction(150),
        SwitchOffAction([leds_segment[1]]), WaitAction(300),
        SwitchOffAction([leds_segment[0]])
    ]
)


leds_ring1 = create_colored_leds([Led(0),Led(1),Led(2),Led(3),Led(4),Led(5),Led(6)],Color('#960000'))
leds_ring2 = create_colored_leds([Led(19),Led(20),Led(21),Led(22),Led(23),Led(24),Led(25)],Color('#960000'))
leds_ring3 = create_colored_leds([Led(26),Led(27),Led(28),Led(29),Led(30),Led(31),Led(32)],Color('#960000'))
leds_ring4 = create_colored_leds([Led(33),Led(34),Led(35),Led(36),Led(37),Led(38),Led(39)],Color('#960000'))
ring_effect = LoopEffect("Proton Pack - Red Ring",
    [
        DimInAction(leds_ring1, 1.5),
        WaitAction(100),
        DimOutAction(leds_ring4, 1.5),
        WaitAction(700),
        DimInAction(leds_ring2, 1.5),
        WaitAction(100),
        DimOutAction(leds_ring1, 1.5),
        WaitAction(700),
        DimInAction(leds_ring3, 1.5),
        WaitAction(100),
        DimOutAction(leds_ring2, 1.5),
        WaitAction(700),
        DimInAction(leds_ring4, 1.5),
        WaitAction(100),
        DimOutAction(leds_ring3, 1.5),
        WaitAction(700)
    ],
    [
        SwitchOffAction(leds_ring1),
        SwitchOffAction(leds_ring2),
        SwitchOffAction(leds_ring3),
        SwitchOffAction(leds_ring4)
    ]
)
ring_override_effect = LoopEffect("Proton Pack - Red Ring OVERRIDE",
    [
        SwitchOnOffAction(leds_ring1, 300),
        SwitchOnOffAction(leds_ring2, 300),
        SwitchOnOffAction(leds_ring3, 300),
        SwitchOnOffAction(leds_ring4, 300)
    ],
    [
        SwitchOffAction(leds_ring1),
        SwitchOffAction(leds_ring2),
        SwitchOffAction(leds_ring3),
        SwitchOffAction(leds_ring4)
    ]
)

leds_tower = [Led(7),Led(8),Led(9),Led(10),Led(11),Led(12),Led(13),Led(14),Led(15),Led(16),Led(17),Led(18)]
tower_effect = LoopEffect("Proton Pack - Charge Tower",
    [
        SwitchOnAction(create_colored_leds(leds_tower, Color('#00008B'))),
        WaitAction(300),
        SwitchOnAction(create_colored_leds(leds_tower, Color('#6082B6'))),
        WaitAction(30)
    ],
    [
        SwitchOffAction(leds_tower)
    ]
)

leds_pack_segment = create_colored_leds([Led(40),Led(41),Led(42),Led(43),Led(44),Led(45),Led(46),Led(47),Led(48),Led(49),Led(50),Led(51),Led(52),Led(53),Led(54),Led(55)], Color('#000022'))
pack_segment_effect = LoopEffect("Proton Pack - Segment",
    [
        SwitchOnAction([leds_pack_segment[1]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[2]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[3]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[4]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[5]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[6]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[7]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[8]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[9]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[10]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[11]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[12]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[13]]), WaitAction(30),
        SwitchOnAction([leds_pack_segment[14]]), WaitAction(30),
        WaitAction(100),
        SwitchOffAction([leds_pack_segment[14]]), WaitAction(30),
        SwitchOffAction([leds_pack_segment[13]]), WaitAction(30),
        SwitchOffAction([leds_pack_segment[12]]), WaitAction(30),
        SwitchOffAction([leds_pack_segment[11]]), WaitAction(30)
    ],
    [
        SwitchOffAction(leds_pack_segment)
    ]
)
pack_segment_override_effect = LoopEffect("Proton Pack - Segment OVERRIDE",
    [
        SwitchOnAction([leds_pack_segment[1]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[2]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[3]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[4]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[5]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[6]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[7]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[8]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[9]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[10]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[11]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[12]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[13]]), WaitAction(5),
        SwitchOnAction([leds_pack_segment[14]]), WaitAction(5),
        WaitAction(100),
        SwitchOffAction([leds_pack_segment[14]]), WaitAction(5),
        SwitchOffAction([leds_pack_segment[13]]), WaitAction(5),
        SwitchOffAction([leds_pack_segment[12]]), WaitAction(5),
        SwitchOffAction([leds_pack_segment[11]]), WaitAction(5)
    ],
    [
        SwitchOffAction(leds_pack_segment)
    ]
)

# ============ SOUNDTRACK - Pack 1

stroke_leds_ring_all = [Led(0),Led(1),Led(2),Led(3),Led(4),Led(5),Led(6),Led(19),Led(20),Led(21),Led(22),Led(23),Led(24),Led(25),Led(26),Led(27),Led(28),Led(29),Led(30),Led(31),Led(32),Led(33),Led(34),Led(35),Led(36),Led(37),Led(38),Led(39)]
stroke_leds_tower = [Led(7),Led(8),Led(9),Led(10),Led(11),Led(12),Led(13),Led(14),Led(15),Led(16),Led(17),Led(18)]
snd_leds_ring1 = [Led(0),Led(1),Led(2),Led(3),Led(4),Led(5),Led(6)]
snd_leds_ring2 = [Led(19),Led(20),Led(21),Led(22),Led(23),Led(24),Led(25)]
snd_leds_ring3 = [Led(26),Led(27),Led(28),Led(29),Led(30),Led(31),Led(32)]
snd_leds_ring4 = [Led(33),Led(34),Led(35),Led(36),Led(37),Led(38),Led(39)]

start_actions_pack1 = [
    WaitAction(300),
    DimInAction(create_colored_leds(stroke_leds_ring_all, Color("#D00003")), 1.15),
    WaitAction(200),
    DimOutAction(create_colored_leds(stroke_leds_ring_all, Color("#D00003")), 1.15),
    WaitAction(400)    
]
for i in range(0,8):
    start_actions_pack1 += [        
        SwitchOnAction(create_colored_leds(snd_leds_ring1, Color("#D00003"))),
        SwitchOnAction(create_colored_leds(snd_leds_ring2, Color('#D00003'))),
        WaitAction(450),
        SwitchOffAction(snd_leds_ring1),
        SwitchOffAction(snd_leds_ring2),
        SwitchOnAction(create_colored_leds(snd_leds_ring3, Color("#D00003"))),
        SwitchOnAction(create_colored_leds(snd_leds_ring4, Color('#D00003'))),
        WaitAction(450),
        SwitchOffAction(snd_leds_ring3),
        SwitchOffAction(snd_leds_ring4)
    ]
start_actions_pack1 += [  
    WaitAction(120)    
]
for i in range(0,16):
    start_actions_pack1 += [        
        SwitchOnAction(create_colored_leds(stroke_leds_tower, Color("#D00003"))),
        SwitchOnAction(create_colored_leds(stroke_leds_ring_all, Color("#0A00D0"))),
        WaitAction(35),
        SwitchOffAction(stroke_leds_tower),
        SwitchOffAction(stroke_leds_ring_all),
        WaitAction(35)
    ]
for i in range(0,4):
    start_actions_pack1 += [     
        SwitchOffAction(snd_leds_ring4),   
        SwitchOnAction(create_colored_leds(snd_leds_ring1, Color("#D00003"))),
        SwitchOnAction(create_colored_leds(stroke_leds_tower, Color("#007F2A"))),
        WaitAction(480),
        SwitchOffAction(snd_leds_ring1),
        SwitchOnAction(create_colored_leds(snd_leds_ring2, Color("#007F2A"))),
        WaitAction(480),
        SwitchOffAction(snd_leds_ring2),
        SwitchOnAction(create_colored_leds(stroke_leds_tower, Color("#3100D0"))),
        SwitchOnAction(create_colored_leds(snd_leds_ring3, Color("#FFF948"))),
        WaitAction(480),
        SwitchOffAction(snd_leds_ring3),
        SwitchOnAction(create_colored_leds(snd_leds_ring4, Color("#3100D0"))),
        WaitAction(480)
    ]
start_actions_pack1 += [ 
    SwitchOffAction(stroke_leds_ring_all),
    SwitchOffAction(stroke_leds_tower),
    WaitAction(1000)    
]
soundtrack_effect_pack1 = LoopEffect("Soundtrack effects - Pack 1",
    start_actions_pack1,
    [
        SwitchOffAction(stroke_leds_ring_all),
        SwitchOffAction(stroke_leds_tower)
    ]
)

# ============ SOUNDTRACK - Pack 2

snd_leds_pack_segment = [Led(40),Led(41),Led(42),Led(43),Led(44),Led(45),Led(46),Led(47),Led(48),Led(49),Led(50),Led(51),Led(52),Led(53),Led(54),Led(55)]

start_actions_pack2 = [
    WaitAction(2250)
]
for i in range(0,8):
    start_actions_pack2 += [
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[i*2],snd_leds_pack_segment[(i*2)+1]], Color("#EA2C2C"))),
        WaitAction(1000),
    ]
start_actions_pack2 += [
    SwitchOffAction(snd_leds_pack_segment),
    WaitAction(120)
]
for i in range(0,16):
    start_actions_pack2 += [     
        SwitchOnAction(create_colored_leds(snd_leds_pack_segment, Color("#EA2C2C"))),
        WaitAction(35),
        SwitchOffAction(snd_leds_pack_segment),
        WaitAction(35)
    ]
for i in range(0,8):
    start_actions_pack2 += [
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[3]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[4]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[5]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[6]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[7]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[8]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[9]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[10]],Color("#007F2A"))), WaitAction(40),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[11]],Color("#FB001D"))), WaitAction(20),
        SwitchOnAction(create_colored_leds([snd_leds_pack_segment[12]],Color("#FB001D"))), WaitAction(20),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[12]],Color("#FB001D"))), WaitAction(20),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[11]],Color("#FB001D"))), WaitAction(20),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[10]],Color("#007F2A"))), WaitAction(40),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[9]],Color("#007F2A"))), WaitAction(40),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[8]],Color("#007F2A"))), WaitAction(40),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[7]],Color("#007F2A"))), WaitAction(40),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[6]],Color("#007F2A"))), WaitAction(40),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[5]],Color("#007F2A"))), WaitAction(40),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[4]],Color("#007F2A"))), WaitAction(40),
        SwitchOffAction(create_colored_leds([snd_leds_pack_segment[3]],Color("#007F2A"))), WaitAction(40),
        WaitAction(20),
    ]
start_actions_pack2 += [ 
    SwitchOffAction(snd_leds_pack_segment),
    WaitAction(1000)    
]    
soundtrack_effect_pack2 = LoopEffect("Soundtrack effects - Pack 2",
    start_actions_pack2,
    [
        SwitchOffAction(snd_leds_pack_segment)
    ]
)


# ============ STROKE - Pack

stroke_pack_leds = [Led(0),Led(1),Led(2),Led(3),Led(4),Led(5),Led(6),Led(19),Led(20),Led(21),Led(22),Led(23),Led(24),Led(25),Led(26),Led(27),Led(28),Led(29),Led(30),Led(31),Led(32),Led(33),Led(34),Led(35),Led(36),Led(37),Led(38),Led(39), \
                Led(7),Led(8),Led(9),Led(10),Led(11),Led(12),Led(13),Led(14),Led(15),Led(16),Led(17),Led(18), \
                Led(40),Led(41),Led(42),Led(43),Led(44),Led(45),Led(46),Led(47),Led(48),Led(49),Led(50),Led(51),Led(52),Led(53),Led(54),Led(55)]

start_actions_pack_stroke = [
    SwitchOnAction(create_colored_leds(stroke_pack_leds, Color("#D00003"))),
    WaitAction(100),
    SwitchOffAction(stroke_pack_leds),
    WaitAction(100),
    SwitchOnAction(create_colored_leds(stroke_pack_leds, Color("#0000D0"))),
    WaitAction(100),
    SwitchOffAction(stroke_pack_leds),
    WaitAction(100), 
    SwitchOnAction(create_colored_leds(stroke_pack_leds, Color("#00D042"))),
    WaitAction(100),
    SwitchOffAction(stroke_pack_leds),
    WaitAction(100),  
    SwitchOnAction(create_colored_leds(stroke_pack_leds, Color("#FFFFFF"))),
    WaitAction(100),
    SwitchOffAction(stroke_pack_leds),
    WaitAction(100),  
]
stroke_effect_pack = LoopEffect("Stroke effects - Pack",
    start_actions_pack_stroke,
    [
        SwitchOffAction(stroke_pack_leds),
    ]
)



# ============ STROKE - Thrower

stroke_thrower_leds = [Led(0),Led(1),Led(2),Led(3),Led(4),Led(5),Led(6),Led(7),Led(8),Led(9), \
               Led(10),Led(11),Led(12),Led(13),Led(14),Led(15),Led(16),Led(17),Led(18)]

start_actions_thrower_stroke = [
    WaitAction(100),
    SwitchOnAction(create_colored_leds(stroke_thrower_leds, Color("#D00003"))),
    WaitAction(100),
    SwitchOffAction(stroke_thrower_leds),
    WaitAction(100),
    SwitchOnAction(create_colored_leds(stroke_thrower_leds, Color("#0000D0"))),
    WaitAction(100),
    SwitchOffAction(stroke_thrower_leds),
    WaitAction(100), 
    SwitchOnAction(create_colored_leds(stroke_thrower_leds, Color("#00D042"))),
    WaitAction(100),
    SwitchOffAction(stroke_thrower_leds),
    WaitAction(100),  
    SwitchOnAction(create_colored_leds(stroke_thrower_leds, Color("#FFFFFF"))),
    WaitAction(100),
    SwitchOffAction(stroke_thrower_leds),
]
stroke_effect_thrower = LoopEffect("Stroke effects - thrower",
    start_actions_thrower_stroke,
    [
        SwitchOffAction(stroke_thrower_leds),
    ]
)