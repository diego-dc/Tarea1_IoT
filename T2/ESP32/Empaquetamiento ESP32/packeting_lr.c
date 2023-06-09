#include <sensors.c>
#include <math.h>
#include <stdlib.h>
#include <sys/time.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"

unsigned short lengmsg[6] = {2, 6, 16, 20, 44, 12016};

unsigned short dataLength(char protocol){
    return lengmsg[(unsigned int)protocol] - 1;
}

unsigned short messageLength(char protocol){
    return 1 + 12 + dataLength(protocol);
}

// Arma un paquete para el protocolo de inicio, que busca solo respuesta
char* dataprotocol00(char* head){
    // seteo del header
    char* ID = "D1";
    memcpy((void*)&(head[0]), (void*)ID, 2);
    uint8_t* MACaddrs = malloc(6);
    esp_efuse_mac_get_default(MACaddrs);
    memcpy((void*)&(head[2]), (void*)MACaddrs, 6); // consigue el MACaddrs
    free(MACaddrs);
    head[8] = 0;
    head[9] = 0;
    unsigned short dataLen = dataLength(0);
    memcpy((void*)&(head[10]), (void*)&dataLen, 2);

    char* msg = malloc(dataLength(0));
    msg[0] = 1;
    return msg;
}

// Arma un paquete para el protocolo 0, con la bateria
char* dataprotocol0(char* head){
    // seteo del header
    char* ID = "D1";
    memcpy((void*)&(head[0]), (void*)ID, 2);
    uint8_t* MACaddrs = malloc(6);
    esp_efuse_mac_get_default(MACaddrs);
    memcpy((void*)&(head[2]), (void*)MACaddrs, 6); // consigue el MACaddrs
    free(MACaddrs);
    head[8] = 0;
    head[9] = 1;
    unsigned short dataLen = dataLength(1);
    memcpy((void*)&(head[10]), (void*)&dataLen, 2);

    // seteamos el largo de la data (6 bytes)
    char* msg = malloc(dataLength(1));
    msg[0] = 1; // 1 byte

    float batt = batt_sensor();
    msg[1] = batt; // 1 byte

    struct timeval current_time;
    gettimeofday(&current_time, NULL);
    time_t time = current_time.tv_sec;
    memcpy((void*)&(msg[2]), (void*)&time, 4); // 4 bytes

    return msg;
}

char* dataprotocol1(char* head){
    // seteo del header
    char* ID = "D1";
    memcpy((void*)&(head[0]), (void*)ID, 2);
    uint8_t* MACaddrs = malloc(6);
    esp_efuse_mac_get_default(MACaddrs);
    memcpy((void*)&(head[2]), (void*)MACaddrs, 6); // consigue el MACaddrs
    free(MACaddrs);
    head[8] = 0;
    head[9] = 2;
    unsigned short dataLen = dataLength(2);
    memcpy((void*)&(head[10]), (void*)&dataLen, 2);
    free(MACaddrs);

    //seteamos el largo de la data (16 bytes)
    char* msg = malloc(dataLength(2));
	msg[0] = 1; //1 byte

    float batt = batt_sensor();
    msg[1] = batt; //1 byte

	struct timeval current_time;
	gettimeofday(&current_time, NULL);
	time_t time = current_time.tv_sec;
	memcpy((void*) &(msg[2]), (void*) &time, 4); //4 bytes

	char temp = THPC_sensor_temp(); //1 byte
	msg[6] = temp;

	float press = THPC_sensor_pres();
    memcpy((void*) &(msg[7]), (void*) &press, 4); //4 bytes

	char hum = THPC_sensor_hum();
    msg[11] = hum;

	float co = THPC_sensor_co2();
    memcpy((void*) &(msg[12]), (void*) &co, 4); //4 bytes

    return msg;

}