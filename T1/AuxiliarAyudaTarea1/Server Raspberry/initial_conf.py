import sqlite3 as sql

def save_conf():
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Conf (ProtocolId, TransportLayer) VALUES (?, ?)",
            (2, 0)
            )
        con.commit()