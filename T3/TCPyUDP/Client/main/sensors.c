#include <math.h>
#include <stdlib.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"

/*

Aqui generamos los 5 tipos de protocolos con sus datos.
Las timestamps en realidad siempre mandamos 0, y por comodidad
guardamos la timestampo del tiempo de llegada en el servidor de la raspberry.


En general los "mensajes" los creamos copiando a la mala (con memcpy) la memoria de los datos en un char*.
No es muy elegante pero funciona.

Al final lo único que se usa fuera de este archivo es:

message: dado un protocolo, crea un mensaje (con header y datos) codificado en un array de bytes (char*).
messageLength: dado un protocolo, entrega el largo del mensaje correspondiente

*/



/* Para un float aleatorio en el intervalo [min, max]*/


float floatrand(float min, float max){
    return min + (float)rand()/(float)(RAND_MAX/(max-min));
}

float* acc_sensor_acc_x(){
    float* arr = malloc(2000* sizeof(float));
    for (int i =0; i <2000; i++){
        arr[i] = floatrand(-16,16);
    }
    return arr;
}

float* acc_sensor_acc_y(){
    float* arr = malloc(2000* sizeof(float));
    for (int i =0; i <2000; i++){
        arr[i] = floatrand(-16,16);
    }
    return arr;
}

float* acc_sensor_acc_z(){
    float* arr = malloc(2000* sizeof(float));
    for (int i =0; i <2000; i++){
        arr[i] = floatrand(-16,16);
    }
    return arr;
}

float* rgyr_x(){
    float* arr = malloc(2000* sizeof(float));
    for (int i =0; i <2000; i++){
        arr[i] = floatrand(-1000,1000);
    }
    return arr;
}

float* rgyr_y(){
    float* arr = malloc(2000* sizeof(float));
    for (int i =0; i <2000; i++){
        arr[i] = floatrand(-1000,1000);
    }
    return arr;
}

float* rgyr_z(){
    float* arr = malloc(2000* sizeof(float));
    for (int i =0; i <2000; i++){
        arr[i] = floatrand(-1000,1000);
    }
    return arr;
}

/*
    Funciones que simulan el THPC_Sensor
    Existe una para cada parametro.
    - temperatura
    - humedad
    - presion
    - co2
*/

char THPC_sensor_temp(){
    char n = (char) 5 + (rand() % 26);
    return n;
}

char THPC_sensor_hum(){
    char n = (char) 30 + (rand() % 51);
    return n;
}

int32_t THPC_sensor_pres(){
    char n = (char) 1000 + (rand() % 201);
    return n;
}

float THPC_sensor_co2(){
    float n = floatrand(30, 200);
    return n;
}

/*
    Funciones que simulan el Batt_sensor
    nivel de bateria del aparato.
*/

uint8_t batt_sensor(){
    char n = (char) 1 + (rand() %100);
    return n;
}

/*
    Funciones que simulan el Acelerometer_kp
*/

float acc_kpi_amp_x() {
    float amp_x = floatrand(0.0059, 0.12);
    return amp_x;
}

float acc_kpi_frec_x() {
    float frec_x = floatrand(0.0059, 0.12);
    return frec_x;
}

float acc_kpi_amp_y() {
    float amp_y = floatrand(29.0, 31.0);
    return amp_y;
}

float acc_kpi_frec_y() {
    float frec_y = floatrand(0.0041, 0.11);
    return frec_y;
}

float acc_kpi_amp_z() {
    float amp_z = floatrand(59.0, 61.0);
    return amp_z;
}

float acc_kpi_frec_z() {
    float frec_z = floatrand(89.0, 91.0);
    return frec_z;
}

float acc_kpi_rms() {
    float RMS = (float) sqrt(pow(acc_kpi_amp_x(), 2) + pow(acc_kpi_amp_y(), 2) + pow(acc_kpi_amp_z(), 2));
    return RMS;
}
