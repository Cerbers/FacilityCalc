import materials as mats
# initializing materials
Coke = mats.Coke
Cmat = mats.Cmat
PCmat = mats.PCmat
A1 = mats.A1
A2 = mats.A2
A3 = mats.A3
A4 = mats.A4
Steel = mats.Steel
A5 = mats.A5


class Outlaw:
    cost = {
        "PCmat": 10,
        "A1": 10,
        "A4": 10
    }
    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        a1_total_coal = A1.total_coal()
        a4_total_salvage = A4.total_salvage()

        # Calculate total basic resources
        total_salvage = pc_total_salvage + A1.cost["Salvage"] * cls.cost["A1"] + a4_total_salvage * cls.cost["A4"]
        total_coal = a1_total_coal * cls.cost["A1"]

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
        }

class SPG:
    cost = {
        "Steel": 150,
        "A5": 85,
        "A4": 40,
        "A3": 65
    }
    @classmethod
    def total_basic_resources(cls):
        steel_totals = Steel.total_basic_resources()
        steel_total = {k: v * cls.cost["Steel"] for k, v in steel_totals.items()}
        a5_totals = A5.total_basic_resources()
        a5_total = {k: v * cls.cost["A5"] for k, v in a5_totals.items()}
        a4_total_salvage = A4.total_salvage() * cls.cost["A4"]
        a3_total_salvage = A3.total_salvage() * cls.cost["A3"]

        # Calculate total basic resources
        total_salvage = steel_total["Salvage"] + a5_total["Salvage"] + a4_total_salvage + a3_total_salvage
        total_coal = steel_total["Coal"] + a5_total["Coal"]
        total_sulfur = steel_total["Sulfur"] + a5_total.get("Sulfur", 0) + a3_total_salvage

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur
        }

class Skycaller:
    cost = {
        "PCmat": 10,
        "A1": 10,
        "A3": 8
    }

    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        a1_total_coal = A1.total_coal()
        a3_total_sulfur = A3.cost["Sulfur"]

        # Calculate total basic resources
        total_salvage = pc_total_salvage + A1.cost["Salvage"] * cls.cost["A1"] + A3.total_salvage() * cls.cost["A3"]
        total_coal = a1_total_coal * cls.cost["A1"]
        total_sulfur = a3_total_sulfur * cls.cost["A3"]

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur
        }