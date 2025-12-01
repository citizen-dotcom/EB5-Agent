# This will create eb5.db and apply all tables from schema.sql.
# Note: You only need to run this once per new database. After that, the EB‑5 Agent will use eb5.db automatically.

import sqlite3

with open("schema.sql", "r") as f:
    schema = f.read()

conn = sqlite3.connect("eb5.db")
conn.executescript(schema)
conn.commit()
conn.close()

print("Database initialized with schema.sql")