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
def parseData(packet, attempts=1):
    print("\n")
    print("------- COMENZANDO DESEMPAQUETAMIENTO ----------\n")
    header = packet[:12]
    data = packet[12:]
    print(f"- Header bytes: {header} " )
    print(f"- Data bytes:  {data}" )
    print("\n--- Recuperando Header --- ")
    headerD = headerDict(header)
    if data:
        print(f"\n--- Recuperando data - ID_protocol({headerD['protocol']}) --- ")
        dataD = dataDict(headerD["protocol"], data)
        if dataD is not None:
            for key,value in dataD.items():
                print(f'{key} : {value}')
    if dataD is not None and dataD["val"] is not 0: # si es 0 es un saludo
        print("\n---------- Guardando Data -----------\n")
        save_data(headerD, dataD)
        print("se guarda data")
        save_log(headerD, dataD)
        print("se guarda logs")
        # esto puede estar mal, ya que, si rellenamos la perdida de paquetes siempre sera el mismo size.
        print("\n------------ Desempaquetamiento Exitoso ------------\n")
        return (headerD,dataD)
    if dataD is None :
        print("\n-- ES UN SALUDO --\n")
        # quizas está malo el paquete
        return (None,None)
    else: {**headerD, **dataD}

def protUnpack(protocol:int, data):
    # cada uno representa la forma de hacer unpack a cada protocolo. [0, 1, 2, 3, 4]
    # ver si estan bien o probar estos  "<BBl", "<BBlBfBf", "<BBlBfBff","<BBlBfBff6f"
    protocol_unpack = ["<BBl", "<BBlBfBf", "<BBlBfBff", "<BBlBfBffffffff", "<BBlBfBf2000f2000f2000f2000f2000f2000f"]
    print("protocolo unpack :" + protocol_unpack[protocol])
    print("data to unpack: " + str(data))
    return unpack(protocol_unpack[protocol], data)

def headerDict(data):
    id_device, M1, M2, M3, M4, M5, M6, transport_layer, protocol, leng_msg = unpack("<2s6BBBH", data)
    # ver si es necesario
    #ID_Dev = int(ID_Dev.decode('ascii')[1])
    # esto porque el MAC va separado por puntos
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    protocol=int(chr(protocol))
    transport_layer=int(chr(transport_layer))
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

            if (protocol==5):

                unp=list(unp)
                lista_floatsACCx=unp[7:2007]
                lista_floatsACCy=unp[2007:4007]
                lista_floatsACCz=unp[4007:6007]

                lista_floatsRgrx=unp[6007:8007]
                lista_floatsRgry=unp[10007:12007]
                lista_floatsRgrz=unp[12007:14007]

                stringfloatAccx="["+";".join(map(str,lista_floatsACCx))+"]"
                stringfloatAccy="["+";".join(map(str,lista_floatsACCy))+"]"
                stringfloatAccz="["+";".join(map(str,lista_floatsACCz))+"]"

                stringfloatRgrx="["+";".join(map(str, lista_floatsRgrx))+"]"
                stringfloatRgry="["+";".join(map(str, lista_floatsRgry))+"]"
                stringfloatRgrz="["+";".join(map(str, lista_floatsRgrz))+"]"

                unp= unp[0:7]

                unp.append(stringfloatAccx)
                unp.append(stringfloatAccy)
                unp.append(stringfloatAccz)

                unp.append(stringfloatRgrx)
                unp.append(stringfloatRgry)
                unp.append(stringfloatRgrz)


            return {key:val for (key,val) in zip(keys, unp)}
        return p

    # el "OK" es un 1 que indica el incio de los datos, se puede utilizar como 0 para señalizar otra cosa
    p1 = ["val", "Batt_level", "Timestamp"] #creo que esto es equivalente(?)
    p2 = ["val","Batt_level","Timestamp","Temp","Press","Hum","Co"]
    p3 = ["val","Batt_level","Timestamp","Temp","Press","Hum","Co","RMS"]
    p4 = ["val","Batt_level","Timestamp","Temp","Press","Hum","Co","RMS","Ampx","Frecx","Ampy","Frecy","Ampz","Frecz"]
    p5 = ["val","Batt_level","Timestamp","Temp","Press","Hum","Co","Accx","Accy","Accz","Rgyrx","Rgyry","Rgyrz"]
    p = [p1, p2, p3, p4, p5]

    try:
        return protFunc(protocol, p[protocol - 1])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None
