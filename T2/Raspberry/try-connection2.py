import time
import logging
import pygatt
from gattlib import DiscoveryService, GATTRequester

service = DiscoveryService("hci0")
devices = service.discover(2)
target = ''

print("Dispositivos encontradoss:")
for address, name in devices.items():
    print("nombre: {}, address: {}".format(name, address))
    if name == "ESP_GATTS_DEMO":
        print("Se encontró la esp32")
        mac = target
        break

print("Conectando con la esp")
req = GATTRequester(mac)

req.exchange_mtu(100)
req.set_mtu(100)

req.write_by_handle(0x2A, bytes('SOMETHING'))
package = req.read_by_handle(0x2a)[0] 

# MAC = '4C:EB:D6:62:15:BA'
# def conectarMac():
#         # se conecta mediante BLE a un dispostivo disponible
#         ##pygatt
#         logging.basicConfig()
#         logging.getLogger('pygatt').setLevel(logging.DEBUG)
#         qty = 0
#         while(qty<1000):
#             try:
#                 adapter = pygatt.GATTToolBackend()
#                 adapter.start()
#                 device = adapter.connect(MAC, address_type=pygatt.BLEAddressType.random,timeout=7.0)
#                 print('Se conecto!')
#                 characteristics = device.discover_characteristics()
#                 for i in characteristics.keys():
#                     print('Caracteristicas: '+str(i))#list(characteristics.keys())))
#                 time.sleep(1)
#                 qty = 100
#             except pygatt.exceptions.NotConnectedError:
#                 qty += 1
#                 print("Se han fallado:", qty, "intentos" )
#                 print("Not connected")
#                 time.sleep(1)
#             finally:
#                 adapter.stop()
#         print("Termino de test de conexión")

# conectarMac()