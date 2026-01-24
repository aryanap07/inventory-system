import pandas as pd
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def run():
    #csv-read
    parts = pd.read_csv("data/parts_master.csv")
    outward = pd.read_csv("data/outward_log.csv")
    part_ids = parts["part_id"].astype(str).tolist()
    completer = WordCompleter(part_ids, ignore_case=True)

    #loop
    while True:
        #user-stock-input
        part_id = prompt("Enter part_id: ", completer=completer)
        qty = int(input("Enter quantity: "))

        #check
        if part_id not in parts["part_id"].values:
            print("❌ Invalid part_id")

        new_item = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "part_id": part_id,
            "quantity": qty
        }

        #processing outward
        outward = pd.concat([outward, pd.DataFrame([new_item])])
        outward.to_csv("data/outward_log.csv", index=False)

        print("✅ Outward stock added successfully")

        #options
        more = input("Add another part? (y/n): ").lower()
        if more != "y":
            print("↩ Returning to Employee Dashboard...\n")
            return        

if __name__ == "__main__":
    run()