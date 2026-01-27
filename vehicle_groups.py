from typing import Type
from products import (
    Outlaw, Chieftain, Thornfall, Blinder, Skycaller, RAC, King_Jester, Flame_BT, MG_BT, SPG, 
    StormCannon, IntelCenter, UndergroundFortress, RSC, Warden_Submarine, Frigate, Bluefin, Longhook, Bowhead, Prod, Firebrand
)

Warden: dict[str, Type[Prod]] = {
    "Outlaw": Outlaw,
    "Chieftain": Chieftain,
    "Thornfall": Thornfall,
    "ATHT": Blinder,
    "Skycaller": Skycaller,
    "RAC": RAC,
    "King Jester": King_Jester,
    "Flame BT": Flame_BT,
    "MG BT": MG_BT,
    "SPG": SPG,
    "Nakki": Warden_Submarine,
    "Frigate": Frigate,
    "Firebrand": Firebrand
}

Colonial: dict[str, Type[Prod]] = {}

All: dict[str, Type[Prod]] = {
    "Bluefin": Bluefin,
    "Longhook": Longhook,
    "Bowhead": Bowhead,
    "RSC": RSC,
    "SC": StormCannon,
    "IC": IntelCenter,
    "UF": UndergroundFortress
}
