from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from services.supabase_client import supabase


def run():

    try:
        parts_data = supabase.table("parts_master").select("part_id").execute().data
        part_ids = [p["part_id"] for p in parts_data]

        completer = WordCompleter(part_ids, ignore_case=True)

    except Exception as e:
        print("❌ DB fetch error:", e)
        return

    while True:
        try:
            customer = input("Enter Customer Name: ")

            part_id = prompt(
                "Enter part_id: ",
                completer=completer
            )

            if part_id not in part_ids:
                print("❌ Invalid part_id")
                continue

            qty = int(input("Enter quantity: "))

            if qty <= 0:
                print("❌ Quantity must be positive")
                continue

            data = {
                "part_id": part_id,
                "quantity": qty,
                "customer": customer
                }

            supabase.table("outward_log").insert(data).execute()

            print("✅ Outward stock saved to cloud!")

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
