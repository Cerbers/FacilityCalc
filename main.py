import products as prods
from tkinter import *

root = Tk()

basic_resources = ("Salvage", "Coal", "Sulfur")

# initializing products
Outlaw = prods.Outlaw
Skycaller = prods.Skycaller
SPG = prods.SPG


Products = {
    "Outlaw": Outlaw,
    "Skycaller": Skycaller,
    "SPG": SPG
}
list_of_products = list(Products.keys())
def main_loop():
    while True:
        calcList = dict()
        print("Available vehicles: Outlaw, Skycaller, SPG")

        while True:
            print("type: 'next' to skip to next category")
            choice = input(f"Choose a vehicle {list_of_products}: ").strip()
            if choice not in list_of_products and choice != 'next':
                # If the choice is not in the list of products, prompt again
                print(f"Invalid choice. Please choose from {list_of_products}.")
                continue
            pick_number = input(f"How many {choice} do you want to build? ")
            if choice in Products:
                calcList[choice] = int(pick_number)
                print(f"You chose: {pick_number} {choice}")
            elif choice == 'next' or pick_number == 'next':
                break
            else:
                print("Invalid choice. Please choose either 'Outlaw' or 'Skycaller'.")
                continue
        print("Calculating resources needed...")
        print(calcList)

        # calculate the total resources needed
        for product_name, amount in calcList.items():
            product_class = Products[product_name]
            if hasattr(product_class, 'total_basic_resources'):
                resources = product_class.total_basic_resources()
                #multiply resources by amount
                resources = {k: v * amount for k, v in resources.items()}
                print(f"{product_name} x{amount}: {resources}")
            else:
                print(f"{product_name} x{amount}: No reource calculation")
        break

#main_loop()

# root window title and dimension
root.title("Vehicle Resource Calculator")
# Set geometry(widthxheight)
root.geometry("400x400")
# adding a label to the root window
lbl = Label(root, text=f"Available vehicles: {', '.join(list_of_products)}")
lbl.grid()
# adding Entry Field
#txt = Entry(root, width=20)
#txt.grid(column=1,row=0)




root.mainloop()