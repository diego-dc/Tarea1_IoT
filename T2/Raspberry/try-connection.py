import time
import logging
import pygatt

MAC = '4C:EB:D6:62:15:BA'

class Controller:

    def __init__(self, parent):
        self.adapter = pygatt.GATTToolBackend() ##pygatt

    def conectarMac(self):
            # se conecta mediante BLE a un dispostivo disponible
            ##pygatt
            logging.basicConfig()
            logging.getLogger('pygatt').setLevel(logging.DEBUG)
            qty = 0
            while(qty<1000):
                try:
                    adapter = pygatt.GATTToolBackend()
                    self.adapter.start()
                    #device = adapter.connect(MAC, address_type=pygatt.BLEAddressType.random,timeout=7.0)
                    device = self.adapter.connect('4C:EB:D6:62:0B:B2',timeout=2.0)
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


cont = Controller()   
cont.conectarMac()