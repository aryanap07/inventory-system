from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from services.supabase_client import supabase


def run():

    try:
        # Fetch data for autocomplete
        parts_data = supabase.table("parts_master").select("part_id").execute().data
        dist_data = supabase.table("distributor_list").select("distributors").execute().data

        part_ids = [p["part_id"] for p in parts_data]
        distributors = [d["distributors"] for d in dist_data]

        part_completer = WordCompleter(part_ids, ignore_case=True)
        dist_completer = WordCompleter(distributors, ignore_case=True)

    except Exception as e:
        print("❌ DB fetch error:", e)
        return

    while True:
        try:
            distributor_select = prompt(
                "Enter Distributor Name: ",
                completer=dist_completer
            )

            if distributor_select not in distributors:
                print("❌ Invalid distributor")
                continue

            part_id = prompt(
                "Enter part_id: ",
                completer=part_completer
            )

            if part_id not in part_ids:
                print("❌ Invalid part_id")
                continue

            qty = int(input("Enter Quantity: "))

            if qty <= 0:
                print("❌ Quantity must be positive")
                continue

            # Insert to Supabase
            data = {
                "part_id": part_id,
                "quantity": qty,
                "distributor": distributor_select
                }

            supabase.table("inward_log").insert(data).execute()

            print("✅ Inward stock saved to cloud!")

            more = input("Add another? (y/n): ").lower()
            if more != "y":
                print("↩ Returning...\n")
                return

        except ValueError:
            print("❌ Enter valid number")

        except Exception as e:
            print("⚠ Error:", e)


if __name__ == "__main__":
    run()
