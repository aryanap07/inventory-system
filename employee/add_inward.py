from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from services.supabase_client import supabase


def cancel(x):
    return x.lower() == "cancel"


def run():

    # load parts & distributors once
    try:
        parts = supabase.table("parts_master").select("part_id").execute().data
        dists = supabase.table("distributor_list").select("distributors").execute().data

        part_ids = [p["part_id"] for p in parts]
        distributors = [d["distributors"] for d in dists]

        part_comp = WordCompleter(part_ids, ignore_case=True)
        dist_comp = WordCompleter(distributors, ignore_case=True)

    except Exception as e:
        print("DB error:", e)
        return

    while True:

        # distributor input
        while True:
            dist = prompt("Distributor (cancel to stop): ",
                          completer=dist_comp,
                          complete_while_typing=True)

            if cancel(dist):
                return

            if dist in distributors:
                break

            print("Invalid distributor")

        # part id input
        while True:
            pid = prompt("Part ID: ",
                         completer=part_comp,
                         complete_while_typing=True)

            if cancel(pid):
                return

            if pid in part_ids:
                break

            print("Invalid part ID")

        # quantity input
        while True:
            q = input("Quantity: ")

            if cancel(q):
                return

            try:
                qty = int(q)

                if qty <= 0:
                    print("Must be positive")
                    continue

                break

            except ValueError:
                print("Enter a number")

        # save entry
        try:
            supabase.table("inward_log").insert({
                "part_id": pid,
                "quantity": qty,
                "distributor": dist
            }).execute()

            print("Saved")

        except Exception as e:
            print("Insert failed:", e)
            continue

        if input("Add more? (y/n): ").lower() != "y":
            return


if __name__ == "__main__":
    run()
