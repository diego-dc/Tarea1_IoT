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
            cur.execute("""
            SELECT
                *
            FROM Configuration
            """)

            respuesta = cur.fetchone()

            if respuesta is not None:
                status = respuesta[1]
                print("status: " + str(status))
                protocol = respuesta[2]
                print("protocol: " + str(protocol))
                discontinous_time = respuesta[7]
                print("discontinous_time: " + str(discontinous_time))
                tcp_port = respuesta[8]
                print("tcp_port: " + str(tcp_port))
                udp_port = respuesta[9]
                print("udp_port: " + str(udp_port))
                return (status, protocol, discontinous_time, tcp_port, udp_port)
            else:
                print("tabla vacía")
                return

        except Exception as e:
            print("Algo salio mal en read_conf")
            print(e)
            return

        finally:
            if con:
                con.close()


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
                "INSERT INTO Configuration (Id_device, Status_conf, Protocol_conf, Acc_sampling, Acc_sensibility, Gyro_sensibility, BME688_sampling, Discontinous_time, TCP_port, UDP_port, Host_ip_addr, Ssid, Pass) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                (1, 21, 2, 10, 2, 200, 1, 1, 3002, 3004, "192.168.100.155", "raspberry_pi", "grupo-iot")
            )
            con.commit()
            print("Se ingreso con exito")
        except Exception as e:
            print("Ocurrió un error creando la configuración inicial")
            print(e)

        finally:
            if con:
                con.close()

def update_conf(conf_dict):
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
                SET Status_conf = %s,
                    Protocol_conf = %s,
                    Acc_sampling = %s,
                    Acc_sensibility = %s,
                    Gyro_sensibility = %s,
                    BME688_sampling = %s,
                    Discontinous_time = %s,
                    TCP_port = %s,
                    UDP_port = %s,
                    Host_ip_addr = %s,
                    Ssid = %s,
                    Pass = %s
                LIMIT 1
                ''',
                (
                    conf_dict["Status_conf"],
                    conf_dict["Protocol_conf"],
                    conf_dict["Acc_sampling"],
                    conf_dict["Acc_sensibility"],
                    conf_dict["Gyro_sensibility"],
                    conf_dict["BME688_sampling"],
                    conf_dict["Discontinuous_time"],
                    conf_dict["TCP_port"],
                    conf_dict["UDP_port"],
                    conf_dict["Host_ip_addr"],
                    conf_dict["Ssid"],
                    conf_dict["Pass"]
                )
            )
            con.commit()
            print("Se actualizó correctamente!")
        except Exception as e:
            print("Ocurrió un error actualizando la configuración en la DB")
            print(e)
        finally:
            if con:
                con.close()
