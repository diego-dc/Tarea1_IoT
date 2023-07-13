import socket
import Desempaquetamiento as dsmpq
import DatabaseWork as dbw
import time


# --------------- CONFIGURACION PARA TCP ---------------

def initial_conf():
    # "192.168.5.177"  # Standard loopback interface address (localhost)
    HOST = "192.168.100.155"# "localhost"
    PORT = 3000  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, #internet
                    socket.SOCK_STREAM) #TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(50)
    print(f"Listening on {HOST}:{PORT} en Main Server")

    return s


def conf_TCP():
    # "192.168.5.177"  # Standard loopback interface address (localhost)
    HOST = "192.168.100.155"#"localhost"
    PORT = 3002  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, #internet
                    socket.SOCK_STREAM) #TCP
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening on {HOST}:{PORT}")
    return s

# --------------- CONFIGURACION PARA UDP ---------------

def conf_UDP():
    UDP_IP = "192.168.100.155"# "localhost"
    UDP_PORT = 3004

    sUDP = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sUDP.bind((UDP_IP, UDP_PORT))

    print(f"Listening for UDP packets in {UDP_IP}:{UDP_PORT}")
    return sUDP

# --------------- Funcionamiento PARA TCP ---------------

def TCP_connection():
    s = conf_TCP()
    while True:
        conn, addr = s.accept()
        print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
        while True:
            try:
                print("Listo para recibir data...")
                doc = b""
                while True:
                    try:

                        data = conn.recv(1024)
                        # si llegan datos completos, tenemos que trabajarlos.
                        if b'\0' in data:
                            doc += data
                            print("Llegó toda la informacion:")
                            print(data)
                            break
                        else:
                            # si no ha llegado todo el msj tenemos que juntarlo
                            doc += data


                    # manejo de excepciones
                    except TimeoutError:
                        conn.send(b'\0')
                        raise
                    except Exception:
                        conn.send(b'\0')
                        raise

                    conn.send(dsmpq.response(False, 0, 1))

            except ConnectionResetError:
                break

            print("Desempaquetando data...")
            try:

                # los guardamos en un dict el contenido del socket - si los datos son null sera un None-.
                # esto los guarda en la base de datos también.
                dataD = dsmpq.parseData(doc)
                # mandamos respuesta?
                conn.send(dsmpq.response(False, 0, 1))
            except Exception as e:
                print("Excepción:")
                print(e)
                print(str(e))
                break

            #print(f"Enviando {res}")
            #conn.send(dsmpq.response(True, 0, 1))
            break

        conn.close()
        print('Conexión cerrada')
        break

# --------------- Funcionamiento PARA UDP ---------------

def UDP_connection():
    s = conf_UDP()
    while True:
        doc = b""
        while True:
            data,client_address = s.recvfrom(1024)

            if data == b'\0':
                    doc += data
                    print("Llego toda la información")
                    break
            else:
                doc += data

            if doc == b'':
                print("Llego data vacía, termina la conexión")
                break

            print("Desempaquetando data...")
            try:

                dataD = dsmpq.parseData(doc)
            except Exception as e:
                    print("Excepción en parseo/guardado UDP :")
                    print(e)
                    break



# ------------------------- MAIN SERVER ---------------------------------

def main_server():
    s = initial_conf()

    while True:
        print("Aceptando conexion en Main server...")
        conn, addr = s.accept()


        # Elegir la configuración
        print("Esperando configuración socket en Main Server...")
        initial_data = conn.recv(1024)

        if initial_data == b'\0':
            # se maneja la configuracion inicial.
            (protocol,transport_layer) = dbw.read_conf()
            conf = ((str(protocol)+str(transport_layer)).encode())

            #esperamos un poco
            #time.sleep(2)
            # se envia
            conn.send(conf)
            print("Configuración enviada desade Main Server :)")
            conn.close()
            if transport_layer == 0:
                print("Ejecutando server TCP desde Main")
                TCP_connection()

            else:
                print("Ejecutando server UDP desde Main")
                UDP_connection()

        else:
            print("No se recibió soliciticud de configuración inical desde Main Server.")
            conn.close()
            print('Conexión cerrada de Main server')
