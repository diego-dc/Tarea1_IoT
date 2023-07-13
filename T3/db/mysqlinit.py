import mysql.connector

# Establecer la conexión con la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="user-iot",
    password="iot1psw",
    database="IoT_tarea3"
)

# Crear un cursor para ejecutar consultas
cursor = conn.cursor()

# Definir la consulta SQL para crear la tabla

create_conf_table = '''CREATE TABLE Configuration (
    Id_device INTEGER,
    Status_conf INTEGER NOT NULL,
    Protocol_conf INTEGER NOT NULL,
    Acc_sampling INTEGER,
    Acc_sensibility INTEGER,
    Gyro_sensibility INTEGER,
    BME688_sampling INTEGER,
    Discontinous_time INTEGER,
    TCP_port INTEGER,
    UDP_port INTEGER,
    Host_ip_addr INTEGER,
    Ssid VARCHAR(45),
    Pass VARCHAR(45),
    PRIMARY KEY (Id_device)
);'''

create_logs_table = '''CREATE TABLE Log (
    Id_device INTEGER UNIQUE,
    Status_report INTEGER NOT NULL,
    Protocol_report INTEGER NOT NULL,
    Battery_level INTEGER,
    Conf_peripherial INTEGER,
    Time_client DATETIME,
    Time_server TIMESTAMP,
    Configuration_Id_device INTEGER,
    PRIMARY KEY (Id_device),
    FOREIGN KEY (Configuration_Id_device) REFERENCES Configuration (Id_device)
);'''

create_data_1_table = '''CREATE TABLE Data_1 (
    Id_device INTEGER,
    Temperature INTEGER NOT NULL,
    Press INTEGER NOT NULL,
    Hum INTEGER,
    Co FLOAT,
    RMS FLOAT,
    Amp_x FLOAT,
    Freq_x FLOAT,
    Amp_y FLOAT,
    Freq_y FLOAT,
    Amp_z FLOAT,
    Freq_z FLOAT,
    Time_client DATETIME,
    Log_Id_device INTEGER NOT NULL,
    PRIMARY KEY (Id_device),
    FOREIGN KEY (Log_Id_device) REFERENCES Log (Id_device)
);'''

create_data_2_table = '''CREATE TABLE Data_2 (
    Id_device INTEGER,
    Racc_x FLOAT,
    Racc_y FLOAT,
    Racc_z FLOAT,
    Rgyr_x FLOAT,
    Rgyr_y FLOAT,
    Rgyr_z FLOAT,
    Time_client DATETIME,
    Log_Id_device INTEGER NOT NULL,
    PRIMARY KEY (Id_device),
    FOREIGN KEY (Log_Id_device) REFERENCES Log (Id_device)
);'''


create_tables = [create_conf_table, create_data_1_table, create_logs_table, create_data_2_table]

# Ejecutar la consulta para crear las tablas
for create_table in create_tables:
    cursor.execute(create_table)

# Confirmar los cambios en la base de datos
conn.commit()

# Cerrar el cursor y la conexión
cursor.close()
conn.close()