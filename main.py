print("Hello World!")

class BasicResource:
    pass

class CoalRefinery(BasicResource):
    def __init__(self):
        self.name = "Coal to Coke"
    
    def convert(self, coal_amount):
        return coal_amount * 0.9

def mainLoop():
    facilities = {
        "1": CoalRefinery()
        # Add more facilities here
    }
    while True:
        print("Choose a facility:")
        for key, facility in facilities.items():
            print(f"{key}: {facility.name}")
        choice = input("Enter number (or 'q' to quit): ")
        if choice == 'q':
            break
        if choice in facilities:
            amount = float(input("Enter amount to convert: "))
            result = facilities[choice].convert(amount)
            print(f"Result: {result}")
        else:
            print("Invalid choice.")

mainLoop()