from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from services.supabase_client import supabase
from inventory.stock_service import get_current_stock


def cancel(x):
    return x.lower() == "cancel"


def run():

    # load part ids for autocomplete
    try:
        parts = supabase.table("parts_master").select("part_id").execute().data
        part_ids = [p["part_id"] for p in parts]
        comp = WordCompleter(part_ids, ignore_case=True)
    except Exception as e:
        print("DB error:", e)
        return

    while True:

        customer = input("Customer (type cancel to stop): ")
        if cancel(customer):
            return

        # choose part
        while True:
            pid = prompt("Part ID: ", completer=comp, complete_while_typing=True)

            if cancel(pid):
                return

            if pid not in part_ids:
                print("Invalid part ID")
                continue

            stock = get_current_stock(pid)

            if stock == 0:
                print("Out of stock")
                continue

            break

        # choose quantity
        while True:
            q = input("Quantity: ")

            if cancel(q):
                return

            try:
                qty = int(q)

                if qty <= 0:
                    print("Must be positive")
                    continue

                if qty > stock:
                    print(f"Only {stock} available")
                    continue

                break

            except ValueError:
                print("Enter a number")

        # save entry
        try:
            supabase.table("outward_log").insert({
                "part_id": pid,
                "quantity": qty,
                "customer": customer
            }).execute()
            print("Saved")
        except Exception as e:
            print("Insert failed:", e)
            continue

        if input("Add more? (y/n): ").lower() != "y":
            return


if __name__ == "__main__":
    run()
