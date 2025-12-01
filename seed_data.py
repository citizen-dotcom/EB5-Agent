# seed_data.py
import sqlite3

conn = sqlite3.connect("eb5.db")

# Clear all rows from the assets table
conn.execute("DELETE FROM assets")

# Optionally reset the auto‑increment counter (if you want IDs to start fresh)
# conn.execute("DELETE FROM sqlite_sequence WHERE name='assets'")

# Now insert fresh rows
conn.execute("""
INSERT INTO assets (asset_id, case_id, type, address, source)
VALUES ('A1', 'SampleCase', 'house', '123 Main St, Dallas, TX', 'indexed')
""")

conn.execute("""
INSERT INTO assets (asset_id, case_id, type, address, source)
VALUES ('A2', 'SampleCase', 'business', '456 Market St, Dallas, TX', 'indexed')
""")

conn.commit()
conn.close()

print("Assets table cleared and new rows inserted")
