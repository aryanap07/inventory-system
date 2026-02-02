import pandas as pd
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def run():
    #csv-read
    parts = pd.read_csv("data/parts_master.csv")
    distributor = pd.read_csv("data/distributor_list.csv")
    inward = pd.read_csv("data/inward_log.csv")

    part_ids = parts["part_id"].astype(str).tolist()
    completer_parts_id = WordCompleter(part_ids, ignore_case=True)

    distributor_fetch = distributor["distributors"].astype(str).tolist()
    completer_distributor = WordCompleter(distributor_fetch, ignore_case=True)

    #loop
    while True:
    #user-stock-input

        distributor_select = prompt("Enter Distributor Name: ", completer=completer_distributor)
        #distributor-name check
        if distributor_select not in distributor["distributors"].astype(str).values:
            print("❌ Invalid distributor name")
            break 
        
        part_id = prompt("Enter part_id: ", completer=completer_parts_id)
        #part-id check
        if part_id not in parts["part_id"].astype(str).values:
            print("❌ Invalid part-id")
            break
        
        else:
            qty = int(input("Enter Quantity: "))
            new_item = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "part_id": part_id,
                "quantity": qty,
                "distributor": distributor_select
            }
            #processing inward
            inward = pd.concat([inward, pd.DataFrame([new_item])])
            inward.to_csv("data/inward_log.csv", index=False)

            print("✅ Inward stock added successfully")

            #options
            more = input("Add another part? (y/n): ").lower()
            if more != "y":
                print("↩ Returning to Employee Dashboard...\n")
                return

if __name__ == "__main__":
    run()