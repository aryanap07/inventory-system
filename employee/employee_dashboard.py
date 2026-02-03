import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


while True:

    clear()

    print("=" * 50)
    print("     INVENTORY MANAGEMENT SYSTEM")
    print("=" * 50)

    print("\nEmployee Dashboard\n")
    print("1) Add Inward Stock")
    print("2) Add Outward Stock")
    print("3) Exit")

    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        from .add_inward import run as inward
        inward()
        pause()

    elif choice == "2":
        from .add_outward import run as outward
        outward()
        pause()

    elif choice == "3":
        print("\nGoodbye 👋")
        break

    else:
        print("\nInvalid choice")
        pause()
