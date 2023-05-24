def TCP_frag_recv(conn):
    doc = b"" #se almacenan los datos
    while True:
        try:
            conn.settimeout(5) 
            data = conn.recv(1024)#comienza conexion
            if data == b'\0':
                break
            else:
                doc += data
        except TimeoutError:
            conn.send(b'\0')
            raise
        except Exception:
            conn.send(b'\0')
            raise
        conn.send(b'\1')
    return doc 



def UDP_frag_recv(s):
    PACK_LEN = 200 #CAMBIAR PACK LEN
    packages = 8000/PACK_LEN
    doc = b""
    addr = None
    counter = 0
    while True:
        try:
            counter += 1
            # ACA AGREGAR ALGO PARA MANEJAR EL CASO EN QUE SE PIERDAN PAQUETES Y DATOS 

            data, addr = s.recvfrom(1024)
            if data == b'\0':
                break
            else:
                doc += data


        except TimeoutError:
            raise
        except Exception:
            raise
        # s.sendto(b'\1', addr)

    if counter < packages:
        while counter <packages:
            doc += b'\x00'
            counter +=1 
    return (doc, addr)