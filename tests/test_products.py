# this method is more desirable
import os, sys

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))


from products import *
from materials import *

products = [Outlaw, Skycaller, RAC, Chieftain, Thornfall, KingJester, MG_BT, SPG, Blinder, Flame_BT, RSC, ConcLargeStructure]
materilas = [A5, Steel, RareAlloy, ThermalShielding]

def test_products_return_type():
    for prod in products:
        result = prod.total_basic_resources()
        assert isinstance(result, dict), f"{prod} did not return a dict"
        for k, v in result.items():
            assert isinstance(v, int), f"{prod}: {k} value is not int (got {type(v)})"

def test_materials_return_type():
    for prod in materilas:
        result = prod.total_basic_resources()
        assert isinstance(result, dict), f"{prod} did not return a dict"
        for k, v in result.items():
            assert isinstance(v, int), f"{prod}: {k} value is not int (got {type(v)})"
