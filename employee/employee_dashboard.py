while True:
    print("\n------------------Employee Dashboard------------------")
    print("1. Add INWARD Stock")
    print("2. Add OUTWARD Stock")
    print("3. Exit")

    choice = input("Enter your choice(1,2,3): ")

    if choice == "1":
        from add_inward import run as add_inward_run
        add_inward_run()

    elif choice == "2":
        from add_outward import run as add_outward_run
        add_outward_run()
    
    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid Choice")

