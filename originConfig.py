from personalCharacters import characters

config = {
    "mainCharacter": 0,  # must be in between number 0 to len(characters) - 1 (0 is the first character)
    "characters": characters,
    "interact": "g",  # change this if you have binded it to something else eg.mouse button
    "move": "left",  # or "right"
    "blink": "space",
    "meleeAttack": "c",
    "awakening": "v",
    "healthPot": "f1",  # important to put your regen potion on this button
    "healthPotAtPercent": 0.35,  # health threshold to trigger potion
    "healthPotUse": True,  # you want to use True
    "regions": {
        "minimap": (1599, 76, 291, 257),
        "buffs": (625, 780, 300, 60),
        "whole-game": (0, 0, 1920, 1080),
        "chaos-remain-time": (353, 103, 120, 40),
    },
    "clickableAreaX": 160,
    "clickableAreaY": 90,
    "clickableArea": 400,
    "screenCenterX": 960,
    "screenCenterY": 540,
    "minimapCenterX": 1745,
    "minimapCenterY": 204,
    "healthCheckX": 623,
    "healthCheckY": 998,
    "charSwitchX": 400,
    "charSwitchY": 760,
    "charPositions": [
        [760, 440],
        [960, 440],
        [1160, 440],
        [760, 560],
        [960, 560],
        [1160, 560],
        [760, 675],
        [960, 675],
        [1160, 675],
        [760, 560],
        [960, 560],
        [1160, 560],
        [760, 675],
        [960, 675],
        [1160, 675],
    ],
    "charSelectConnectX": 1054,
    "charSelectConnectY": 761,
    "charSelectOkX": 920,
    "charSelectOkY": 640,
}
