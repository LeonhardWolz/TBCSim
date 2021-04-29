import enum

inventory_slot = {
    #0: "Ammo",
    1: "Head",
    2: "Neck",
    3: "Shoulder",
    #4: "Body",
    5: "Chest",
    6: "Waist",
    7: "Legs",
    8: "Feet",
    9: "Wrist",
    10: "Hand",
    11: "Finger1",
    12: "Finger2",
    13: "Trinket1",
    14: "Trinket2",
    15: "Back",
    16: "Mainhand",
    17: "Offhand",
    18: "Ranged",
    #19: "Tabard"
}

inv_type_in_slot = {
    0: (24,),
    1: (1,),
    2: (2,),
    3: (3,),
    4: (4,),
    5: (5, 20),
    6: (6,),
    7: (7,),
    8: (8,),
    9: (9,),
    10: (10,),
    11: (11,),
    12: (11,),
    13: (12,),
    14: (12,),
    15: (16,),
    16: (13, 17, 21),
    17: (13, 14, 17, 22, 23),
    18: (15, 25, 26, 28),
    19: (19,)
}
cast_time = {
    1: 0,
    2: 250,
    3: 500,
    4: 1000,
    5: 2000,
    6: 5000,
    7: 10000,
    8: 20000,
    9: 30000,
    10: 1000,
    11: 2000,
    12: 5000,
    13: 30000,
    14: 3000,
    15: 4000,
    16: 1500,
    18: -1000000,
    19: 2500,
    20: 2500,
    21: 2600,
    22: 3500,
    23: 1800,
    24: 2200,
    25: 2900,
    26: 3700,
    27: 4100,
    28: 3200,
    29: 4700,
    30: 4500,
    31: 2300,
    32: 7000,
    33: 5125,
    34: 8000,
    35: 12500,
    36: 600,
    37: 25000,
    38: 45000,
    39: 50000,
    50: 1300,
    70: 300000,
    90: 1700,
    91: 2800,
    110: 750,
    130: 1600,
    150: 3800,
    151: 2700,
    152: 3100,
    153: 3400,
    170: 8000,
    171: 6000,
    190: 100,
    191: 0,
    192: 15000,
    193: 12000,
    194: -1000000,
    195: 1100,
    196: 750,
    197: 850,
    198: 900,
    199: 333}

duration_index = {
    1: 10000,
    2: 300000010,
    3: 60000,
    4: 120000,
    5: 300000,
    6: 600000,
    7: 5000000,
    8: 15000,
    9: 30000,
    10: 60000000,
    11: 100000000,
    12: 30000000,
    13: 6000000,
    14: 12000000,
    15: 30000000,
    16: 230000,
    17: 5000000,
    18: 20000,
    19: 3000000,
    20: 60000000,
    21: -1,
    22: 45000,
    23: 90000,
    24: 160000,
    25: 180000,
    26: 240000,
    27: 3000,
    28: 5000,
    29: 12000,
    30: 1800000,
    31: 8000,
    32: 6000,
    35: 4000,
    36: 1000,
    37: 1,
    38: 11000,
    39: 2000,
    40: 1200000,
    41: 360000,
    42: 3600000,
    62: 75000,
    63: 25000,
    64: 40000,
    65: 1500,
    66: 2500,
    85: 18000,
    86: 21000,
    105: 9000,
    106: 24000,
    125: 35000,
    145: 2700000,
    165: 7000,
    185: 6000,
    186: 2000,
    187: 0,
    205: 27000,
    225: 604800000,
    245: 50000,
    265: 55000,
    285: 1000,
    305: 14000,
    325: 36000,
    326: 44000,
    327: 500,
    328: 250,
    347: 900000,
    367: 7200000,
    387: 16000,
    407: 100,
    427: -600000,
    447: 2000,
    467: 22000,
    468: 26000,
    487: 1700,
    507: 1100,
    508: 1100,
    527: 14400000,
    547: 5400000,
    548: 10800000,
    549: 3800,
    550: 2147483647,
    551: 3500,
    552: 210000,
    553: 6000,
    554: 155000,
    555: 4500,
    556: 28000,
    557: 165000,
    558: 114000,
    559: 53000,
    560: 299000,
    561: 3300000,
    562: 150000,
    563: 20500,
    564: 13000,
    565: 70000,
    566: 0,
    567: 135000,
    568: 1250,
    569: 280000,
    570: 32000,
    571: 5500,
    572: 100000,
    573: 9999,
    574: 200,
    575: 17000,
    576: 43200000,
    580: 64800000
}


class PlayerClass(enum.Enum):
    Warrior = 1
    Paladin = 2
    Hunter = 3
    Rogue = 4
    Priest = 5
    Shaman = 7
    Mage = 8
    Warlock = 9
    Druid = 11


class Race(enum.Enum):
    Human = 1
    Orc = 2
    Dwarf = 3
    Nightelf = 4
    Undead = 5
    Tauren = 6
    Gnome = 7
    Troll = 8
    Bloodelf = 10
    Draenei = 11


class CombatAction(enum.Enum):
    Idle = 0
    Cast_Spell = 1
    Wand_Attack = 2
    Consume_Item = 3


socket_color_name = {
    1: "Meta",
    2: "Red",
    4: "Yellow",
    8: "Blue"
}

ignite_dmg_pct = {
    11119: 8,
    11120: 16,
    12846: 24,
    12847: 32,
    12848: 40
}

socket_bitmask = {
    1: 1,
    2: 2,
    3: 4,
    4: 8
}
