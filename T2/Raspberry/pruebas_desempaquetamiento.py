import Desempaquetamiento as dsmpq

import struct

def print_mensaje(data):
    ID = data[0:2]
    MACAddress = data[2:8]
    TransportLayer = data[8]
    IDProtocol = data[9]
    DataLength = data[10:12]
    print(f"ID: {str(ID)}")
    print(f"MAC Address: {str(MACAddress)}")
    print(f"Transport Layer: {str(TransportLayer)}")
    print(f"ID Protocol: {str(IDProtocol)}")
    print(f"Data Length: {str(DataLength)}")
    print(f"Data: {data[13:]}")


msj_00 = b'\x44\x31\x4C\xEB\xD6\x62\x15\xBA\x10\x00\x14\x00\x00' # SALUDO - id_protocol => 0
msj_0 = b'\x44\x31\x4C\xEB\xD6\x62\x15\xBA\x30\x01\x06\x00\x01\x64\x7E\x89\xF4\x00' # id_protocol => 1
msj_1 = b'\x44\x29\x4C\xEB\xD6\x62\x15\xBA\x30\x02\x06\x00\x01\x64\x7E\x89\xF4\x00\x14\x00\x00\x03\xe8\x05\x21\x03\x15\x03' # id_protocol => 2
msj_2 = b'\x44\x30\x4C\xEB\xD6\x62\x15\xBA\x30\x03\x06\x00\x01\x64\x7E\x89\xF4\x00\x17\x26\x32\x24\x23\x12\x21\x03\x15\x03\x02\x3d\xd6\x40' # id_protocol => 3
msj_3 = b'\x44\x33\x4C\xEB\xD6\x62\x15\xBA\x30\x04\x06\x00\x01\x64\x7E\x89\xF4\x00\x19\x64\x32\x24\x23\x08\x21\x03\x15\x03\x02\x3d\xd6\x40\xcd\xcc\x50\x3f\xcd\xb4\x0e\x3e\x33\x99\x40\x00\xcd\xce\x91\x3f\x3e\x0c\xcc\x40\x00\x1d\x4d\x40' # id_protocol => 4
#       |2-IDdevice| 6 - MAC |1TL|1IDp|2LengM |1val|1Btl|4TS|1Temp|4Press|1Hum|4Co|4Rms|4ampx|4frecx|4ampy|4frecy|4ampz|frecz|


msj_prueba = msj_3

print("\n------------------ Utilizando mensaje  -------------\n")
print("largo: " + str(len(msj_prueba)))
print_mensaje(msj_prueba)
dsmpq.parseData(msj_prueba)



