print("Hello World!")

basic_resources = ("Salvage", "Coal", "Sulfur")

class Coke:
    cost = {
        "Coal": 1.21
    }

class Cmat:
    cost = {
        "salvage": 5
    }

class A1:
    cost = {
        "Salvage": 15,
        "Coke": 75
    }
    @classmethod
    def total_coal(cls):
        # Get total coal from Coke class
        total_coal = cls.cost["Coke"] * Coke.cost["Coal"]
        return total_coal

class A2:
    pass

class A3:
    cost = {
        "Cmat": 3,
        "Sulfur": 20
    }
    @classmethod
    def total_salvage(cls):
        # Get total salvage from Cmat class
        total_salvage = cls.cost["Cmat"] * Cmat.cost["salvage"]
        return total_salvage

class A4:
    pass

class A5:
    pass

class PCmat:
    cost = {
        "Cmat": 15,
        "Salvage": 25 # this is a innacurate value, in place of 'metal beam'
    }

    @classmethod
    def total_salvage(cls):
        # Get Salvage from Cmat class
        cmat_salvage = Cmat.cost["salvage"]
        # Add own salvage
        total = cls.cost["Salvage"] + (cmat_salvage * cls.cost["Cmat"])
        return total



class Skycaller:
    cost = {
        "PCmat": 10,
        "A1": 10,
        "A3": 8
    }

    @classmethod
    def total_basic_resources(cls):
        # Get total salvage from PCmat
        pc_total_salvage = PCmat.total_salvage() * cls.cost["PCmat"]
        # Get total coal from A1
        a1_total_coal = A1.total_coal()
        # Get total sulfur from A3
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

print(Skycaller.total_basic_resources())  # Testing the total_basic_resources method
