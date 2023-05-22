import socket
import Desempaquetamiento as dsmpq
import juntarFragm as jf
import DatabaseWork as dbw

# los tipos de protocolo, dejar acá el actual.
protocol = "-1"

# el tipo de conexión que se realizará.
# true -> TCP
# false -> UDP
transport_layer = True

# --------------- CONFIGURACION PARA TCP ---------------

def conf_TCP():
    # "192.168.5.177"  # Standard loopback interface address (localhost)
    HOST = "192.168.245.177"#"localhost"
    PORT = 5000  # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, #internet
                    socket.SOCK_STREAM) #TCP
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening on {HOST}:{PORT}")
    return s

# --------------- CONFIGURACION PARA UDP ---------------

def conf_UDP():
    UDP_IP = "192.168.5.177"# "localhost"
    UDP_PORT = 5010

    sUDP = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sUDP.bind((UDP_IP, UDP_PORT))

    print(f"Listening for UDP packets in {UDP_IP}:{UDP_PORT}")
    return sUDP

# --------------- Funcionamiento PARA TCP ---------------

def TCP_connection():
    global protocol
    s = conf_TCP()
    conn, addr = s.accept()
    print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
    while True:
        try:
            # vemos que protocolo debería llegar.
            if protocol != "4":
                data = conn.recv(1024)
                # si llegan datos completos, tenemos que trabajarlos.
                if b'\0' in data:
                    print(data)
                    # los guardamos en un dict el contenido del socket - si los datos son null sera un None-.
                    # esto los guarda en la base de datos también.
                    dataD = dsmpq.parseData(data)

                    # Este sería el caso de un saludo.
                    if (dataD["OK"] == 0):
                        print('es un saludo')
                        print(f"Recibido {data}") 
                        # extraemos de la db la conf a utilizar. 
                        res = dbw.read_conf()
                        print(f"Enviando {res}")
                        res = dsmpq.confResponse(res[0], res[1]) # revisar si esta tomando bien los datos.
                        # enviamos la conf al cliente.
                        conn.send(res.encode())
                        break

            else:
                data = jf.TCP_frag_recv(conn)
                dataD = dsmpq.parseData(data)

        except ConnectionResetError:
            break
        print(f"Recibido afuera {data}")
        res = dbw.read_conf()
        print(f"Enviando {res}")
        conn.send(dsmpq.response(True, 0, 1))

        # revisar protocolo y tipo de conexion a usar.
        protocol = res[0]
        if res[1] == "0" :
            transport_layer = True

        if res[1] == "1" :
            transport_layer = False
            break

    conn.close()
    print('Desconectado')

# --------------- Funcionamiento PARA UDP ---------------

def UDP_connection():
    while True:
        while True:
            sUDP = conf_UDP()
            if protocol != "4":
                data, client_address = sUDP.recvfrom(1)
                dataD = dsmpq.parseData(data)

            else:
                data = jf.UDP_frag_recv(sUDP)
                dataD = dsmpq.parseData(data)

            print(f"Recibido {data}")

            # leemos la tabla de config
            res = dbw.read_conf()

            # revisar protocolo y tipo de conexion a usar.
            protocolo = res[0]
            if res[1] == "0" :
                transport_layer = True

            if res[1] == "1" :
                transport_layer = False
                break




while True:
    # Elegir la configuración
    print("Configurando socket según corresponda")

    if transport_layer:
        TCP_connection()

    elif not transport_layer:
        UDP_connection()

    # presionar una tecla para terminar el programa(?)
    # no se si con la Raspberry funcionara
    # quizas que cambie una variable y aqui terminar el programa. y checkear en los otrs whiles.
