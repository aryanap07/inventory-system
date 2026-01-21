import pandas as pd
from datetime import datetime

def run():
    #csv-read
    parts = pd.read_csv("Inventory-system/data/parts_master.csv")
    inward = pd.read_csv("Inventory-system/data/inward_log.csv")

    while True:
        #user-stock-input
        part_id = input("Enter part_id: ")
        qty = int(input("Enter Quantity: "))

        if part_id not in parts["part_id"].values:
            print("❌ Invalid part_id")
        
        new_item = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "part_id": part_id,
            "qty": qty
        }


        inward = pd.concat([inward, pd.DataFrame([new_item])])
        inward.to_csv("Inventory-system/data/inward_log.csv", index=False)

        print("✅ Inward stock added successfully")
        
        more = input("Add another part? (y/n): ").lower()
        if more != "y":
            print("↩ Returning to Employee Dashboard...\n")
            return

