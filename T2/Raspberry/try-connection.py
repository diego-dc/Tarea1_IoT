import time
import logging
import pygatt

MAC = '4C:EB:D6:62:15:BA'
def conectarMac():
        # se conecta mediante BLE a un dispostivo disponible
        ##pygatt
        logging.basicConfig()
        logging.getLogger('pygatt').setLevel(logging.DEBUG)
        qty = 0
        while(qty<1000):
            try:
                adapter = pygatt.GATTToolBackend()
                adapter.start()
                device = adapter.connect(MAC, address_type=pygatt.BLEAddressType.random,timeout=2.0)
                print('Se conecto!')
                characteristics = device.discover_characteristics()
                for i in characteristics.keys():
                    print('Caracteristicas: '+str(i))#list(characteristics.keys())))
                time.sleep(1)
                qty = 100
            except pygatt.exceptions.NotConnectedError:
                qty += 1
                print("Se han fallado:", qty, "intentos" )
                print("Not connected")
                time.sleep(1)
            finally:
                adapter.stop()
        print("Termino de test de conexión")

conectarMac()