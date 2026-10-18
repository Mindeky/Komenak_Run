
LEVELS = [
    {
        "name": "Civics class",
        "milk": 15,
        "enemies": [{"image": "blazej.png", "powers": False}],
    },
    {
        "name": "Blazej's lounge",
        "milk": 20,
        "enemies": [{"image": "blazej.png", "powers": True}],
        "powerups": ["shield"],
    },
    {
        "name": "Detention",
        "milk": 15,
        "enemies": [
            {"image": "blazej.png", "powers": False},
            {"image": "chamilka.jpg", "powers": False, "y": 100},
        ],
        "powerups": ["shield","fastP"],
    },
    {
        "name": "Principals office",
        "milk": 20,
        "enemies": [
            {"image": "blazej.png", "powers": True},
            {"image": "chamilka.jpg", "powers": True},
        ],
        "powerups": ["shield","slowE","fastP"],
    },
    {
        "name": "MACURA BOSSFIGHT",
        "milk": 50,
        "enemies": [],
        "boss": {"image": "macura.jpg",},
        "powerups": ["shield"],
    }
]