from characters import characters

config = {
    "mainCharacter": 0,  # must be in between number 0 to len(characters) - 1 (0 is the first character)
    "enableMultiCharacterMode": True,  # this is lit
    "floor3Mode": False,  # only enable if you ONLY want to run infinite floor3 clearing
    "characters": characters,
    "performance": False,  # set True for lower-end PCs
    "interact": "g",  # change this if you have binded it to something else eg.mouse button
    "move": "left",  # or "right"
    "blink": "space",
    "meleeAttack": "c",
    "awakening": "v",
    "healthPot": "f1",  # important to put your regen potion on this button
    "friends": "u",
    "invisible": True,
    "healthPotAtPercent": 0.35,  # health threshold to trigger potion
    "auraRepair": True,  # True if you have aura, if not then for non-aura users: MUST have your character parked near a repairer in city before starting the script
    "shortcutEnterChaos": True,  # you want to use True
    "useHealthPot": True,  # you want to use True
    "regions": {
        "minimap": (1655, 170, 260, 200),
        "abilities": (625, 779, 300, 155),
        "leaveMenu": (0, 154, 250, 300),
        "buffs": (625, 780, 300, 60),
        "center": (685, 280, 600, 420),
        "portal": (228, 230, 1370, 570),
    },
    "screenResolutionX": 1920,
    "screenResolutionY": 1080,
    "clickableAreaX": 500,
    "clickableAreaY": 250,
    "screenCenterX": 960,
    "screenCenterY": 540,
    "minimapCenterX": 1772,
    "minimapCenterY": 272,
    "timeLimit": 450000,  # to prevent unexpected amount of time spent in a chaos dungeon, a tiem limit is set here, will quit after this amount of seconds
    "timeLimitAor": 720000,  # to prevent unexpected amount of time spent in a chaos dungeon, a tiem limit is set here, will quit after this amount of seconds
    "blackScreenTimeLimit": 30000,  # if stuck in nothing for this amount of time, alt f4 game, restart and resume.
    "delayedStart": 2500,
    "portalPause": 700,
    "healthCheckX": 690,
    "healthCheckY": 854,
    "charSwitchX": 400,
    "charSwitchY": 760,
    "charPositionsAtCharSelect": [
        [500, 827],
        [681, 827],
        [874, 827],
        [1050, 827],
        [1237, 827],
        [1425, 827],
    ],
    "charPositions": [
        [760, 440],
        [960, 440],
        [1160, 440],
        [760, 530],
        [960, 530],
        [1160, 530],
        [760, 620],
        [960, 620],
        [1160, 620],
        [760, 530],
        [960, 530],
        [1160, 530],
        [760, 620],
        [960, 620],
        [1160, 620],
    ],
    "charSelectConnectX": 1054,
    "charSelectConnectY": 761,
    "charSelectOkX": 920,
    "charSelectOkY": 640,
}
