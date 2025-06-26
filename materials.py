basic_resources = ("Salvage", "Coal", "Sulfur", "Rare Metals") # reminder of what the objects are breakdowned to

# TODO: unify materials

class Coke:
    cost = {
        "Coal": 1.21
    }

class Cmat:
    cost = {
        "Salvage": 5
    }

class PCmat:
    cost = {
        "Cmat": 15,
        "Salvage": 25 # this is a innacurate value, in place of 'metal beam'
    }

    @classmethod
    def total_salvage(cls):
        cmat_salvage = Cmat.cost["Salvage"]
        total = cls.cost["Salvage"] + (cmat_salvage * cls.cost["Cmat"])
        return total

class A1:
    cost = {
        "Salvage": 15,
        "Coke": 75
    }
    @classmethod
    def total_coal(cls):
        # Get total coal from Coke class
        total_coal = cls.cost["Coke"] * Coke.cost["Coal"]
        return int(total_coal)

class A2:
    cost = {
        "Salvage": 15
    }

class A3:
    cost = {
        "Cmat": 3,
        "Sulfur": 20
    }
    @classmethod
    def total_salvage(cls):
        # Get total salvage from Cmat class
        total_salvage = cls.cost["Cmat"] * Cmat.cost["Salvage"]
        return total_salvage

class A4:
    cost = {
        "PCmat": 1
    }
    @classmethod
    def total_salvage(cls):
        # Get total salvage from PCmat class
        total_salvage = PCmat.total_salvage()
        return total_salvage

class Steel:
    cost = {
        "PCmat": 3,
        "Coke": 125,
        "Sulfur": 60
    }
    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        coke_total_coal = cls.cost["Coke"] * Coke.cost["Coal"]

        # Calculate total basic resources
        total_salvage = pc_total_salvage
        total_coal = coke_total_coal
        total_sulfur = cls.cost["Sulfur"]

        return {
            "Salvage": total_salvage,
            "Coal": int(total_coal),
            "Sulfur": total_sulfur
        }

class A5:
    cost = {
        "Steel": 3,
        "Coke": 245,
        "A1": 10,
        "A2": 10
    }
    @classmethod
    def total_basic_resources(cls):
        total_salvage = cls.cost["Steel"] * Steel.total_basic_resources()["Salvage"] + cls.cost["A1"] * A1.cost["Salvage"]  + cls.cost["A2"] * A2.cost["Salvage"]
        total_coal = cls.cost["Coke"] * Coke.cost["Coal"] + cls.cost["A1"] * A1.total_coal()
        total_sulfur = cls.cost["Steel"] * Steel.total_basic_resources()["Sulfur"]

        return {
            "Salvage": total_salvage,
            "Coal": int(total_coal),
            "Sulfur": total_sulfur
        }
    
class RareAlloy:
    cost = {
        "Rare Metals": 20,
        "PCmat": 5,
        "Coke": 60
    }
    @classmethod
    def total_basic_resources(cls):
        total_salvage = cls.cost["PCmat"] * PCmat.total_salvage()
        total_coal = cls.cost["Coke"] * Coke.cost["Coal"]

        return {
            "Salvage": total_salvage,
            "Coal": int(total_coal),
            "Rare Metals": RareAlloy.cost['Rare Metals']
        }

# Intermediate materials below


class ThermalShielding:
    cost = {
        "Cmat": 2,
        "A4": 5
    }
    @classmethod
    def total_basic_resources(cls):
        total_salvage = A4.total_salvage() * cls.cost["A4"] + Cmat.cost["Salvage"] * cls.cost["Cmat"]

        return {
            "Salvage": total_salvage
        }