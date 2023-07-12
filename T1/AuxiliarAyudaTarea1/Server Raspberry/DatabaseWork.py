import datetime
import sqlite3 as sql

# Documentación https://docs.python.org/3/library/sqlite3.html

# agregar conn.commit()?

def save_log(header, data):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO Logs (DeviceId, MAC, TransportLayer, ProtocolId) VALUES (?, ?, ?, ?)",
            (header["ID_device"], header["MAC"], header["transport_layer"], header["protocol"])
        )
        try:
            con.commit()

        except Exception as e:
            print("Error executing SQL query", str(e))


def save_loss(header, data, attempts):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        current_timestamp = datetime.datetime.now().timestamp()
        latency = current_timestamp - data["Timestamp"]
        # TODO guardar cantidad de attempts.
        attempts = 1
        cur.execute(
            "INSERT INTO Loss (Latency, Attempts) VALUES (?, ?)",
            (latency, attempts)
            )
        con.commit()

def save_data(header, data):
    with sql.connect("DB.sqlite") as con:
        protocol = header["protocol"] - 1

        if data is None:
            print("Error: Failed to unpack data for protocol", protocol)
            return

        query = ""
        params = ()

        if protocol == 0:
            query = "INSERT INTO Data (DeviceId, MAC, Val, BattLevel, Timestamp) VALUES (?, ?, ?, ?, ?)"
            params = (header["ID_device"], header["MAC"], data["val"], data["Batt_level"], data["Timestamp"])
        elif protocol == 1:
            query = "INSERT INTO Data (DeviceId, MAC, Val, BattLevel, Timestamp, Temp, Press, Hum, Co) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (header["ID_device"], header["MAC"], data["val"], data["Batt_level"], data["Timestamp"],
                      data["Temp"], data["Pres"], data["Hum"], data["Co"])
        elif protocol == 2:
            query = "INSERT INTO Data (DeviceId, MAC, Val, BattLevel, Timestamp, Temp, Press, Hum, Co, RMS) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (header["ID_device"], header["MAC"], data["val"], data["Batt_level"], data["Timestamp"],
                      data["Temp"], data["Pres"], data["Hum"], data["Co"], data["RMS"])
        elif protocol == 3:
            query = "INSERT INTO Data (DeviceId, MAC, Val, BattLevel, Timestamp, Temp, Press, Hum, Co, RMS, AmpX, FrecX, AmpY, FrecY, AmpZ, FrecZ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (header["ID_device"], header["MAC"], data["val"], data["Batt_level"], data["Timestamp"],
                      data["Temp"], data["Pres"], data["Hum"], data["Co"], data["RMS"],
                      data["amp_x"], data["frec_x"], data["amp_y"], data["frec_y"],
                      data["amp_z"], data["frec_z"])
        elif protocol == 4:
            query = "INSERT INTO Data (DeviceId, MAC, Val, BattLevel, Timestamp, Temp, Press, Hum, Co, AccX, AccY, AccZ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (header["ID_device"], header["MAC"], data["val"], data["Batt_level"], data["Timestamp"],
                      data["Temp"], data["Pres"], data["Hum"], data["Co"],
                      data["acc_x"], data["acc_y"], data["acc_z"])
        else:
            print("Error: Invalid protocol", protocol)
            return

        try:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()

        except Exception as e:
            print("Error executing SQL query", str(e))

def read_conf():
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        res = cur.execute(
            "SELECT * FROM Conf WHERE rowid = 1"
        )

        conf = res.fetchone()
        print(conf)

        return conf

def update_conf(protocol_id, transport_layer):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        cur.execute(
            '''UPDATE Conf
            SET ProtocolId = ?,
                TransportLayer = ?
            WHERE rowid = 1
            ''',
            (protocol_id, transport_layer)
        )
        cur.commit()
