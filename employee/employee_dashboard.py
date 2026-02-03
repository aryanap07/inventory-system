import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


while True:

    clear()

    print("=" * 50)
    print("               STOCKFLOW")
    print("        Inventory Management CLI")
    print("=" * 50)

    print("\nDashboard\n")
    print("1) Add Inward Stock")
    print("2) Add Outward Stock")
    print("3) Check Stock")
    print("4) Exit")

    choice = input("\nSelect option (1-4): ").strip()

    if choice == "1":
        from .add_inward import run as inward
        inward()

    elif choice == "2":
        from .add_outward import run as outward
        outward()

    elif choice == "3":
        from inventory.check_stock import run as stock
        stock()

    elif choice == "4":
        print("\nThanks for using StockFlow 👋")
        break

    else:
        print("\nInvalid choice")
        input("Press Enter to continue...")
