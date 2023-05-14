import socket
import Desempaquetamiento as dsmpq

# --------------- CONFIGURACION PARA TCP ---------------

# "192.168.5.177"  # Standard loopback interface address (localhost)
HOST = "192.168.5.177"#"localhost"
PORT = 5000  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, #internet
                  socket.SOCK_STREAM) #TCP
s.bind((HOST, PORT))
s.listen(5)
print(f"Listening on {HOST}:{PORT}")

# --------------- CONFIGURACION PARA UDP ---------------

""" UDP_IP = "192.168.5.177"# "localhost" 
UDP_PORT = 5010

sUDP = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sUDP.bind((UDP_IP, UDP_PORT))

print(f"Listening for UDP packets in {UDP_IP}:{UDP_PORT}") """

while True:
    conn, addr = s.accept()
    print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
    while True:
        try:
            data = conn.recv(1024)
            # si no se manda ningun dato, se cierra conexión.
            if data == b'':
                break
            
            # si llegan datos completos, tenemos que trabajarlos.
            if b'\0' in data:
                # los guardamos en un dict el contenido del socket - si los datos son null sera un None-. 
                # esto los guarda en la base de datos también.
                dataD = dsmpq.parseData(data)


            # probablemente se puede aprovechar este caso.
            if (dataD == None):
                print('Paquete sin datos.')



        except ConnectionResetError:
            break
        print(f"Recibido {data}")
        conn.send(data.encode())

    conn.close()
    print('Desconectado')
