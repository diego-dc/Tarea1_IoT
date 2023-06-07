import Desempaquetamiento as dsmpq

import struct

def print_mensaje(data):
    ID = data[0:2]
    MACAddress = data[2:8]
    TransportLayer = data[8]
    IDProtocol = data[9]
    DataLength = data[10:12]
    print(f"ID: {ID}")
    print(f"MAC Address: {MACAddress}")
    print(f"Transport Layer: {TransportLayer}")
    print(f"ID Protocol: {IDProtocol}")
    print(f"Data Length: {DataLength}")
    print(f"Data: {msj_00[13:]}")


msj_00 = b'\x44\x31\x4C\xEB\xD6\x62\x15\xBA\x10\x01\x14\x00\x00\x00' # SALUDO - id_protocol => 0
msj_0 = b'\x44\x31\x4C\xEB\xD6\x62\x15\xBA\x30\x01\x06\x00\x4C\x64\x7E\x89\xF4\x00' # id_protocol => 1
msj_1 = b'\x44\x31\x4C\xEB\xD6\x62\x15\xBA\x30\x00\x06\x00\x4C\x64\x7E\x89\xF4\x00\x05\x64\x32\x24\x23\x05\x21\x03\x15\x03' # id_protocol => 2

msj_prueba = msj_0

print("------------------ Utilizando mensaje  -------------")
print_mensaje(msj_prueba)
dsmpq.parseData(msj_prueba)



