import pandas as pd
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def run():
    #csv-read
    parts = pd.read_csv("data/parts_master.csv")
    inward = pd.read_csv("data/inward_log.csv")
    part_ids = parts["part_id"].astype(str).tolist()
    completer = WordCompleter(part_ids, ignore_case=True)


    while True:
        #user-stock-input
        part_id = prompt("Enter part_id: ", completer=completer)
        qty = int(input("Enter Quantity: "))

        if part_id not in parts["part_id"].values:
            print("❌ Invalid part_id")
            
        new_item = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "part_id": part_id,
            "quantity": qty
        }


        inward = pd.concat([inward, pd.DataFrame([new_item])])
        inward.to_csv("data/inward_log.csv", index=False)

        print("✅ Inward stock added successfully")
        
        more = input("Add another part? (y/n): ").lower()
        if more != "y":
            print("↩ Returning to Employee Dashboard...\n")
            return

