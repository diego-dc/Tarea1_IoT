import datetime
import sqlite3 as sql
import mysql.connector

# Documentación https://docs.python.org/3/library/sqlite3.html

# agregar conn.commit()?

def save_log(header, data):
    with mysql.connector.connect(
        host="localhost",
        user="user-iot",
        password="iot1psw",
        database="IoT_tarea3"
    ) as con:
        try:

            # tomamos el status
            cur = con.cursor()
            cur.execute(f"SELECT Status_conf FROM Configuration WHERE Id_device={header['ID_device']}")
            status=cur.fetchone()[0]

            query = "INSERT INTO Log ( Status_report, Protocol_report, Battery_Level, Conf_peripheral, configuration_Id_device )  VALUES(?, ?, ?, ?, ?);"
            params = (status, header["protocol"], data["Batt_level"], None, header["ID_Dev"])
            cur.execute(query, params)

            # recuperamos el id del log
            id_log=cur.lastrowid

            con.commit()
            cur.close()


        except Exception as e:
            print("Error executing SQL query", str(e))
        finally:
         if con:
             con.close()

    return id_log


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
    6 = Discontinous_time,
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
                Discontinous_time,
                TCP_port,
                UDP_port,
                Host_ip_addr,
                Ssid,
                Pass
            FROM Configuration
            """)

            return res.fetchone()
        except Exception as e:
            print("Algo salio mal en read_conf")
            print(e)
            return


def create_initial_conf():
    with mysql.connector.connect(
        host="localhost",
        user="user-iot",
        password="iot1psw",
        database="IoT_tarea3"
    ) as con:
        try:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Configuration (Status_conf, Protocol_conf, Acc_sampling, Acc_sensibility, Gyro_sensibility, BME688_sampling, Discontinous_time, TCP_port, UDP_port, Host_ip_addr, Ssid, Pass) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);",
                (21, 2, 10, 2, 200, 1, 1, 3002, 3004, 192168100155, "raspberry_pi", "grupo-iot")
            )
            cur.commit()
        except Exception as e:
            print("Ocurrió un error creando la configuración inicial")
            print(e)

def update_conf(status_conf, protocol_conf, acc_sampling, acc_sensibility, gyro_sensibility, bme688_sampling, discontinous_time, tcp_port, udp_port, host_ip_addr, ssid, password):
    with mysql.connector.connect(
        host="localhost",
        user="user-iot",
        password="iot1psw",
        database="IoT_tarea3"
    ) as con:
        try:
            cur = con.cursor()
            cur.execute(
                '''UPDATE Configuration
                SET Status_conf = ?,
                    Protocol_conf = ?,
                    Acc_sampling = ?,
                    Acc_sensibility = ?,
                    Gyro_sensibility = ?,
                    BME688_sampling = ?,
                    Discontinous_time = ?,
                    TCP_port = ?,
                    UDP_port = ?,
                    Host_ip_addr = ?,
                    Ssid = ?,
                    Pass = ?
                WHERE rowid = 1
                ''',
                (status_conf, protocol_conf, acc_sampling, acc_sensibility, gyro_sensibility, bme688_sampling, discontinous_time, tcp_port, udp_port, host_ip_addr, ssid, password)
            )
            cur.commit()
        except Exception as e:
            print("Ocurrió un error actualizando la configuración en la DB")
            print(e)
