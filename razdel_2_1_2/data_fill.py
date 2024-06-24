import sqlite3


con = sqlite3.connect('db.sqlite3')
cur = con.cursor()

deflators = [
    (2024, 1.329),
    (2023, 1.257),
    (2022, 1.096)
]
taxes = [
    (1, 0.06),
    (2, 0.08)
]

# sql_update_query = """Update calculator_ratetype set tax_rate = ? where id = ?"""

cur.execute('DELETE FROM calculator_proposal;')
# cur.executemany('INSERT INTO calculator_ratetype VALUES(?, ?);', taxes)
# cur.executemany('INSERT INTO calculator_ratetype VALUES(?, ?);', taxes)

con.commit()
con.close()
