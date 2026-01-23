import pandas as pd
from datetime import datetime

def run():
    parts = pd.read_csv("data/parts_master.csv")
    outward = pd.read_csv("data/outward_log.csv")
    while True:
        part_id = input("Enter part_id: ")
        qty = int(input("Enter quantity: "))

        if part_id not in parts["part_id"].values:
            print("❌ Invalid part_id")

        new_item = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "part_id": part_id,
            "qty": qty
        }

        outward = pd.concat([outward, pd.DataFrame([new_item])])
        outward.to_csv("Inventory-system/data/outward_log.csv", index=False)

        print("✅ Outward stock added successfully")

        more = input("Add another part? (y/n): ").lower()
        if more != "y":
            print("↩ Returning to Employee Dashboard...\n")
            return        
