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


# Parsea la info del paquete recibido
# Retorna null si es null la data.
# Retorna un diccionario del paquete completo si no. 
def parseData(packet):
    header = packet[:10]
    data = packet[10:]
    headerD = headerDict(header)
    dataD = dataDict(headerD["protocol"], data)
    if dataD is not None:
        save_data(headerD, dataD)
        
    return None if dataD is None else {**headerD, **dataD}

def protUnpack(protocol:int, data):
    # cada uno representa la forma de hacer unpack a cada protocolo. [0, 1, 2, 3, 4]
    protocol_unpack = ["<BBf", "<2BfBfBf", "<2BfBfB2f", "2BfBfB8f", "2BfBfB2001f2000f2000f"]
    return unpack(protocol_unpack[protocol], data)

def headerDict(data):
    M1, M2, M3, M4, M5, M6, transport_layer, protocol, leng_msg = unpack("<6B2BH", data)
    # esto porque el MAC va separado por puntos
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    return {"MAC":MAC, "protocol":protocol, "transport_layer":transport_layer, "length":leng_msg}

def dataDict(protocol:int, data):
    if protocol not in [0, 1, 2, 3, 4]:
        print("Error: protocol doesnt exist")
        return None
    def protFunc(protocol, keys):
        def p(data):
            unp = protUnpack(protocol, data)
            return {key:val for (key,val) in zip(keys, unp)}
        return p
    
    # el "OK" es un 1 que indica el incio de los datos, se puede utilizar como 0 para señalizar otra cosa
    p0 = ["OK", "Batt_level", "Timestamp"] #creo que esto es equivalente(?)
    p1 = ["OK", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co"]
    p2 = ["OK", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS"]
    p3 = ["OK", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS", "amp_x", "frec_x", "amp_y", "frec_y", "amp_z", "frec_z"]
    p4 = ["OK", "Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS", "acc_x", "acc_y", "acc_z"]
    p = [p0, p1, p2, p3, p4]

    try:
        return protFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None