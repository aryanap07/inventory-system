from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from services.supabase_client import supabase
from inventory.stock_service import get_current_stock


def run():

    try:
        parts = supabase.table("parts_master") \
            .select("part_id, part_name") \
            .execute().data or []

        if not parts:
            print("No parts found")
            return

        ids = [p["part_id"] for p in parts]
        name_map = {p["part_id"]: p["part_name"] for p in parts}

        comp = WordCompleter(ids, ignore_case=True)

    except Exception as e:
        print("DB error:", e)
        return

    while True:

        pid = prompt(
            "Part ID (cancel to stop): ",
            completer=comp,
            complete_while_typing=True
        )

        if pid.lower() == "cancel":
            return

        if pid not in name_map:
            print("Invalid part ID")
            continue

        stock = get_current_stock(pid)

        print(f"\n{pid} | {name_map[pid]}")
        print(f"Stock: {stock}")

        if stock <= 0:
            print("Out of stock")

        if input("\nCheck another? (y/n): ").lower() != "y":
            return

if __name__ == "__main__":
    run()