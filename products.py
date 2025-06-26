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
Rare_Alloy = mats.RareAlloy
Thermal = mats.ThermalShielding


class Chieftain:
    cost = {
        "PCmat": 5,
        "A1": 10,
        "A4": 8
    }
    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        a1_total_coal = A1.total_coal() * cls.cost["A1"]
        a1_total_salvage = A1.cost["Salvage"] * cls.cost["A1"]
        a4_total_salvage = A4.total_salvage() * cls.cost["A4"]

        # Calculate total basic resources
        total_salvage = pc_total_salvage + a1_total_salvage + a4_total_salvage
        total_coal = a1_total_coal

        return {
            "Salvage": total_salvage,
            "Coal": total_coal
        }

class Thornfall:
    cost = {
        "PCmat": 60,
        "A4": 15,
        "A3": 15,
        "A1": 10
    }
    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        a4_total_salvage = A4.total_salvage() * cls.cost["A4"]
        a3_total_salvage = A3.total_salvage() * cls.cost["A3"]
        a3_total_sulfur = A3.cost["Sulfur"] * cls.cost["A3"]
        a1_total_coal = A1.total_coal() * cls.cost["A1"]
        a1_total_salvage = A1.cost["Salvage"] * cls.cost["A1"]

        # Calculate total basic resources
        total_salvage = a4_total_salvage + a3_total_salvage + a1_total_salvage + pc_total_salvage
        total_coal = a1_total_coal
        total_sulfur = a3_total_sulfur

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur
        }

class Outlaw:
    cost = {
        "PCmat": 10,
        "A1": 10,
        "A4": 10
    }
    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        a1_total_coal = A1.total_coal() * cls.cost["A1"]
        a1_total_salvage = A1.cost["Salvage"] * cls.cost["A1"]
        a4_total_salvage = A4.total_salvage() * cls.cost["A4"]

        # Calculate total basic resources
        total_salvage = pc_total_salvage + a1_total_salvage + a4_total_salvage
        total_coal = a1_total_coal

        return {
            "Salvage": total_salvage,
            "Coal": total_coal
        }

class Blinder:
    cost = {
        "PCmat": 5,
        "A2": 10,
        "A4": 3
    }
    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        a2_total_salvage = A2.cost["Salvage"] * cls.cost["A2"]
        a4_total_salvage = A4.total_salvage() * cls.cost["A4"]
        # Calculate total basic resources
        total_salvage = pc_total_salvage + a2_total_salvage + a4_total_salvage

        return {
            "Salvage": total_salvage
        }

class RAC:
    cost = {
        "PCmat": 35,
        "A1": 10,
        "A3": 8
    }

    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        a1_total_salvage = A1.cost["Salvage"] * cls.cost["A1"]
        a1_total_coal = A1.total_coal() * cls.cost["A1"]
        a3_total_salvage = A3.total_salvage() * cls.cost["A3"]
        a3_total_sulfur = A3.cost["Sulfur"] * cls.cost["A3"]

        # Calculate total basic resources
        total_salvage = pc_total_salvage + a1_total_salvage + a3_total_salvage
        total_coal = a1_total_coal
        total_sulfur = a3_total_sulfur

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
        a1_total_salvage = A1.cost["Salvage"] * cls.cost["A1"]
        a1_total_coal = A1.total_coal() * cls.cost["A1"]
        a3_total_salvage = A3.total_salvage() * cls.cost["A3"]
        a3_total_sulfur = A3.cost["Sulfur"] * cls.cost["A3"]

        # Calculate total basic resources
        total_salvage = pc_total_salvage + a1_total_salvage + a3_total_salvage
        total_coal = a1_total_coal
        total_sulfur = a3_total_sulfur

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur
        }

class KingJester:
    cost = {
        "Steel": 5,
        "A1": 15,
        "A3": 3,
        "RareAlloy": 1
    }
    @classmethod
    def total_basic_resources(cls):
        steel_totals = Steel.total_basic_resources()
        steel_total = {k: v * cls.cost["Steel"] for k, v in steel_totals.items()}
        a1_total_coal = A1.total_coal() * cls.cost["A1"]
        a1_total_salvage = A1.cost['Salvage'] * cls.cost['A1']
        a3_total_sulfur = A3.cost['Sulfur'] * cls.cost['A3']
        a3_total_salvage = A3.total_salvage() * cls.cost["A3"]
        rare_totals = Rare_Alloy.total_basic_resources()
        rare_total = {k: v * cls.cost['RareAlloy'] for k, v in rare_totals.items()}

        total_salvage = steel_total['Salvage'] + a1_total_salvage + a3_total_salvage + rare_total['Salvage']
        total_coal = steel_total["Coal"] + a1_total_coal + rare_total['Coal']
        total_sulfur =  a3_total_sulfur + steel_total['Sulfur']
        total_rares = rare_total['Rare Metals']

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur,
            "Rare Metals": total_rares
        }

class MG_BT:
    cost = {
        "Steel": 50,
        "A5": 35,
        "A4": 60,
        "A3": 30
    }
    @classmethod
    def total_basic_resources(cls):
        steel_totals = Steel.total_basic_resources()
        steel_total = {k: v * cls.cost["Steel"] for k, v in steel_totals.items()}
        a5_totals = A5.total_basic_resources()
        a5_total = {k: v * cls.cost["A5"] for k, v in a5_totals.items()}
        a4_total_salvage = A4.total_salvage() * cls.cost["A4"]
        a3_total_salvage = A3.total_salvage() * cls.cost["A3"]
        a3_total_sulfur = A3.cost["Sulfur"] * cls.cost["A3"]

        # Calculate total basic resources
        total_salvage = steel_total["Salvage"] + a5_total["Salvage"] + a4_total_salvage + a3_total_salvage
        total_coal = steel_total["Coal"] + a5_total["Coal"]
        total_sulfur = steel_total["Sulfur"] + a5_total.get("Sulfur", 0) + a3_total_sulfur

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur
        }

class Flame_BT:
    cost = {
        "Steel": 40,
        "A5": 45,
        "A4": 30,
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
        a3_total_sulfur = A3.cost["Sulfur"] * cls.cost["A3"]

        # Calculate total basic resources
        total_salvage = steel_total["Salvage"] + a5_total["Salvage"] + a4_total_salvage + a3_total_salvage
        total_coal = steel_total["Coal"] + a5_total["Coal"]
        total_sulfur = steel_total["Sulfur"] + a5_total.get("Sulfur", 0) + a3_total_sulfur

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur
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
        a3_total_sulfur = A3.cost["Sulfur"] * cls.cost["A3"]

        # Calculate total basic resources
        total_salvage = steel_total["Salvage"] + a5_total["Salvage"] + a4_total_salvage + a3_total_salvage
        total_coal = steel_total["Coal"] + a5_total["Coal"]
        total_sulfur = steel_total["Sulfur"] + a5_total.get("Sulfur", 0) + a3_total_sulfur
        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur
        }

class RSC:
    cost = {
        "Steel": 285,
        "A5": 105,
        "A4": 105,
        "A3": 95,
        "RareAlloy": 100,
        "Thermal": 45
    }
    @classmethod
    def total_basic_resources(cls):
        steel_totals = Steel.total_basic_resources()
        steel_total = {k: v * cls.cost["Steel"] for k, v in steel_totals.items()}
        a5_totals = A5.total_basic_resources()
        a5_total = {k: v * cls.cost["A5"] for k, v in a5_totals.items()}
        a4_total_salvage = A4.total_salvage() * cls.cost["A4"]
        a3_total_salvage = A3.total_salvage() * cls.cost["A3"]
        a3_total_sulfur = A3.cost["Sulfur"] * cls.cost["A3"]
        rare_totals = Rare_Alloy.total_basic_resources()
        rare_total = {k: v * cls.cost['RareAlloy'] for k, v in rare_totals.items()}
        thermal_salvage = Thermal.total_basic_resources()

        # Calculate total basic resources
        total_salvage = steel_total["Salvage"] + a5_total["Salvage"] + a4_total_salvage + a3_total_salvage + rare_total['Salvage'] + thermal_salvage["Salvage"]
        total_coal = steel_total["Coal"] + a5_total["Coal"] + rare_total['Coal']
        total_sulfur = steel_total["Sulfur"] + a5_total.get("Sulfur", 0) + a3_total_sulfur
        total_rares = rare_total['Rare Metals']

        return {
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Sulfur": total_sulfur,
            "Rare Metals": total_rares
        }

class ConcLargeStructure:
    # default value to be overriden
    cost = {
        "PCmat": 1,
        "RareAlloy": 1,
        "Thermal": 1
    }
    @classmethod
    def total_basic_resources(cls):
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        rare_totals = Rare_Alloy.total_basic_resources()
        rare_total = {k: v * cls.cost['RareAlloy'] for k, v in rare_totals.items()}
        thermal_salvage = Thermal.total_basic_resources()


        total_salvage = pc_total_salvage + rare_total['Salvage'] + thermal_salvage["Salvage"]
        total_coal = rare_total['Coal']
        total_rares = rare_total['Rare Metals']

        return{
            "Salvage": total_salvage,
            "Coal": total_coal,
            "Rare Metals": total_rares
        }

class StormCannon(ConcLargeStructure):
    cost = {
        "PCmat": 300,
        "RareAlloy": 40,
        "Thermal": 45
    }

class UndergroundFortress(ConcLargeStructure):
    cost = {
        "PCmat": 200,
        "RareAlloy": 5,
        "Thermal": 35
    }

class IntelCenter(ConcLargeStructure):
    cost = {
        "PCmat": 50,
        "RareAlloy": 3,
        "Thermal": 15
    }

