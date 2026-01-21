import pandas as pd

df = pd.DataFrame(columns=["date", "part_id", "qty"])
df.to_csv("outward_log.csv", index=False)

print("Empty CSV file created using pandas")
