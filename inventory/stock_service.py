from services.supabase_client import supabase

def get_current_stock(part_id):

    inward = supabase.table("inward_log")\
        .select("quantity")\
        .eq("part_id", part_id)\
        .execute().data

    outward = supabase.table("outward_log")\
        .select("quantity")\
        .eq("part_id", part_id)\
        .execute().data

    total_in = sum(int(i["quantity"]) for i in inward)
    total_out = sum(int(o["quantity"]) for o in outward)

    return total_in - total_out
