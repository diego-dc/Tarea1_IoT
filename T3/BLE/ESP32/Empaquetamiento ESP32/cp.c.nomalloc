#include <stdio.h>

void cpMAC(unsigned char *destino, unsigned char *origen, int longitud) {
    for (int i = 0; i < longitud; i++) {
        destino[i] = origen[i];
    }
}

int main() {
    unsigned char macOrigen[] = {0xA1, 0xB2, 0xC3, 0xD4, 0xE5, 0xF6};
    unsigned char macDestino[6];

    int longitud = sizeof(macOrigen) / sizeof(macOrigen[0]);

    cpMAC(macDestino, macOrigen, longitud);

    printf("MAC original: ");
    for (int i = 0; i < longitud; i++) {
        printf("%02X", macOrigen[i]);
        if (i < longitud - 1) {
            printf(":");
        }
    }

    printf("\nMAC copiada: ");
    for (int i = 0; i < longitud; i++) {
        printf("%02X", macDestino[i]);
        if (i < longitud - 1) {
            printf(":");
        }
    }

    return 0;
}