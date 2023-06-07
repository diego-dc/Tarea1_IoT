from struct import unpack, pack
import traceback
from DatabaseWork import * 

# Documentación struct unpack,pack :https://docs.python.org/3/library/struct.html#
'''
Estas funciones se encargan de parsear y guardar los datos recibidos.
Usamos struct para pasar de un array de bytes a una lista de numeros/strings. (https://docs.python.org/3/library/struct.html)
(La ESP32 manda los bytes en formato little-endian, por lo que los format strings deben empezar con <)

-dataSave: Guarda los datos en la BDD
-response: genera un OK para mandar de vuelta cuando se recibe un mensaje, con posibilidad de pedir que se cambie el status/protocol
-protUnpack: desempaca un byte array con los datos de un mensaje (sin el header)
-headerDict: Transforma el byte array de header (los primeros 10 bytes de cada mensaje) en un diccionario con la info del header
-dataDict: Transforma el byta array de datos (los bytes luego de los primeros 10) en un diccionario con los datos edl mensaje

'''

# se puede ajustar segun lo que decidamos
def response(change:bool=False, status:int=255, protocol:int=255):
    OK = 1
    CHANGE = 1 if change else 0
    return pack("<BBBB", OK, CHANGE, status, protocol)

def confResponse(protocol, transport_layer):
    return pack("<BB", protocol, transport_layer)

# Parsea la info del paquete recibido
# Retorna null si es null la data.
# Retorna un diccionario del paquete completo si no.
def parseData(packet):
    print("------- comenzando desempaquetamiento ----------")
    header = packet[:12]
    data = packet[12:]
    print("- Recuperando Header: ")
    headerD = headerDict(header)
    print(f"- Recuperando data - ID_protocol({headerD['protocol']}): ")
    dataD = dataDict(headerD["protocol"], data)
    if dataD is not None and dataD["val"] is not "0": # si es 0 es un saludo
        print("---------- Guardando Data -----------")
        save_data(headerD, dataD)
        print("se guarda data")
        save_log(headerD, dataD)
        print("se guarda logs")
        # esto puede estar mal, ya que, si rellenamos la perdida de paquetes siempre sera el mismo size.
        data_length = headerD["length"]
        #save_loss(headerD, dataD, data_length)
        #print("se guarda perdida")
        print("------------ Desempaquetamiento Exitoso ------------")

    return None if dataD is None else {**headerD, **dataD}

def protUnpack(protocol:int, data):
    # cada uno representa la forma de hacer unpack a cada protocolo. [0, 1, 2, 3, 4]
    protocol_unpack = ["<B", "<2Bf", "<2BfBfBf", "<2BfBfB2f", "<2BfBfB8f", "<2BfBfB2001f2000f2000f"]
    print("protocolo unpack :" + protocol_unpack[protocol])
    print("data to unpack: " + str(data))
    return unpack(protocol_unpack[protocol], data)

def headerDict(data):
    id_device, M1, M2, M3, M4, M5, M6, transport_layer, protocol, leng_msg = unpack("<h8Bh", data)
    # esto porque el MAC va separado por puntos
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    print("---- HeaderD ---- ")
    print("ID_device:" + str(id_device))
    print("MAC:" + str(MAC))
    print("protocol:" + str(protocol))
    print("transport_layer:" + str(transport_layer))
    print("length:" + str(leng_msg))
    return {"ID_device": id_device, "MAC":MAC, "protocol":protocol, "transport_layer":transport_layer, "length":leng_msg}

def dataDict(protocol:int, data):
    if protocol not in [0, 1, 2, 3, 4, 5]:
        print("Error: protocol doesnt exist")
        return None
    def protFunc(protocol, keys):
        def p(data):
            unp = protUnpack(protocol, data)
            return {key:val for (key,val) in zip(keys, unp)}
        return p

    # el "OK" es un 1 que indica el incio de los datos, se puede utilizar como 0 para señalizar otra cosa
    p0 = ["val"] #creo que esto es equivalente(?)
    p1 = ["val", "Batt_level", "Timestamp"] #creo que esto es equivalente(?)
    p2 = ["val", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co"]
    p3 = ["val", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS"]
    p4 = ["val", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS", "amp_x", "frec_x", "amp_y", "frec_y", "amp_z", "frec_z"]
    p5 = ["val", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS", "acc_x", "acc_y", "acc_z"]
    p = [p0, p1, p2, p3, p4, p5]

    try:
        return protFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None
