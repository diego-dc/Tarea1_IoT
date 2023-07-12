import datetime
import sqlite3 as sql
import mysql.connector

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

def save_data(header, data, id_device):
    # revisar si esto funciona
    with mysql.connector.connect(
        host="localhost",
        user="user-iot",
        password="iot1psw",
        database="IoT_tarea3"
    ) as con:
        
        protocol = header["protocol"] - 1

        if data is None:
            print("Error: Failed to unpack data for protocol", protocol)
            return

        query = ""
        params = ()

        if protocol == 0:
            queries = "INSERT INTO Data_1 (Log_Id_device) VALUES(?)"
            params = (id_device)
        elif protocol == 1:
            queries = "INSERT INTO Data_1 (Temperature, Press, Hum, Co, Time_client, Log_Id_device) VALUES(?, ?, ?, ?, ?, ?);"
            params = (data["Temp"], data["Press"], data["Hum"],data["Co"],data["Timestamp"], id_device)
        elif protocol == 2:
            queries = "INSERT INTO Data_1 (Temperature, Press, Hum, Co, RMS, Time_client, Log_Id_device) VALUES(?, ?, ?, ?, ?, ?, ?);"
            params = (data["Temp"], data["Press"], data["Hum"],data["Co"],data["RMS"],data["Timestamp"], id_device)
        elif protocol == 3:
            queries = "INSERT INTO Data_1 (Temperature, Press, Hum, Co, RMS, Amp_x, Freq_x, Amp_y, Freq_y, Amp_z, Freq_z, Time_client, Log_Id_device) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"
            params = (data["Temp"], data["Press"], data["Hum"],data["Co"],data["RMS"],data["Ampx"],
                        data["Frecx"],data["Ampy"],data["Frecy"],data["Ampz"],
                        data["Frecz"],data["Timestamp"],id_device)
        elif protocol == 4:
            queries = [
                "INSERT INTO Data_1 (Temperature, Press, Hum, Co, Time_client, Log_Id_device) VALUES(?,?,?,?,?,?);",
                "INSERT INTO Data_2 (Racc_x, Racc_y, Racc_z, Rgyr_x, Rgyr_y, Rgyr_z, Time_client, Log_Id_device) VALUES(?,?,?,?,?,?,?,?);"
                ]
            params = [ (data["Temp"], data["Press"], data["Hum"],data["Co"],data["Timestamp"], id_device),
                        (data["Accx"], data["Accy"], data["Accz"], data["Rgyrx"], data["Rgyry"], data["Rgyrz"],data["Timestamp"], id_device)
                ]
        else:
            print("Error: Invalid protocol", protocol)
            return

        try:
            cur = con.cursor()
            for i in range(len(queries)):
                cur.execute(queries[i], params[i])
            con.commit()

        except Exception as e:
            print("Error executing SQL query", str(e))

        finally:
            if con:
                con.close()

def read_conf():
    '''
    0 = Status_conf,
    1 = Protocol_conf,
    2 = Acc_sampling,
    3 = Acc_sensibility,
    4 = Gyro_sensibility,
    5 = BME688_sampling,
    6 = Discontinuos_time,
    7 = TCP_PORT,
    8 = UDP_port,
    9 = Host_ip_addr,
    10 = Ssid,
    11 = Pass
    '''

    with mysql.connector.connect(
        host="localhost",
        user="user-iot",
        password="iot1psw",
        database="IoT_tarea3"
    ) as con:
        
        try: 
        
            cur = con.cursor()
            res = cur.execute("""
            SELECT 
                Status_conf,
                Protocol_conf,
                Acc_sampling,
                Acc_sensibility,
                Gyro_sensibility,
                BME688_sampling,
                Discontinuos_time,
                TCP_PORT,
                UDP_port,
                Host_ip_addr,
                Ssid,
                Pass
            FROM Config
            """)
            
            print(res.fetchone())
            return res.fetchone()
        
        except Exception as e:
            print("Algo salio mal en read_conf")
            print(e)
            return


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
