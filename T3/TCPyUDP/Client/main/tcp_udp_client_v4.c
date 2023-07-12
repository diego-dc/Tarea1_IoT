/*
 * SPDX-FileCopyrightText: 2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Unlicense OR CC0-1.0
 */
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <errno.h>
#include <netdb.h>            // struct addrinfo
#include <arpa/inet.h>
#include "esp_netif.h"
#include "esp_log.h"
#include "esp_sleep.h"
#if defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
#include "addr_from_stdin.h"
#endif

#if defined(CONFIG_EXAMPLE_IPV4)
#define HOST_IP_ADDR CONFIG_EXAMPLE_IPV4_ADDR
#elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
#define HOST_IP_ADDR ""
#endif

#include "packeting.h"
#include "sdkconfig.h"

#define PORT CONFIG_EXAMPLE_PORT

static const char *TAG = "example";

void udp_client(char protocol) {
    while (1) {
        int addr_family = 0;
        int ip_protocol = 0;
#if defined(CONFIG_EXAMPLE_IPV4)
        struct sockaddr_in dest_addr;
        dest_addr.sin_addr.s_addr = inet_addr(HOST_IP_ADDR);
        dest_addr.sin_family = AF_INET;
        dest_addr.sin_port = htons(PORT + 4);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;
#elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
        struct sockaddr_storage dest_addr = { 0 };
        ESP_ERROR_CHECK(get_addr_from_stdin(PORT + 4, SOCK_DGRAM, &ip_protocol, &addr_family, &dest_addr));
#endif
        int sock = socket(addr_family, SOCK_DGRAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket UDP: errno %d", errno);
            break;
        }
                // Set timeout
        struct timeval timeout;
        timeout.tv_sec = 10;
        timeout.tv_usec = 0;
        setsockopt (sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof timeout);

        ESP_LOGI(TAG, "Socket created, sending to %s:%d", HOST_IP_ADDR, PORT + 4);

        while (1) {
            char* payload = malloc(messageLength(protocol));
            char* header = malloc(12);
            char* message;

            int int_protocol = (int)protocol - 48;

            switch (int_protocol) {
                case 1:
                    message = dataprotocol1(header);
                    break;
                case 2:
                    message = dataprotocol2(header);
                    break;
                case 3:
                    message = dataprotocol3(header);
                    break;
                case 4:
                    message = dataprotocol4(header);
                    break;
                case 5:
                    message = dataprotocol4(header);
                    break;
                default:
                    message = dataprotocol1(header);
                    break;
            }
            memcpy((void*)&(payload[0]), (void*)header, 12);
            memcpy((void*)&(payload[12]), (void*)message, dataLength(int_protocol));
            free(header);
            free(message);


            int err = sendto(sock, payload, messageLength(int_protocol), 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)); //setea direccion de destino
            free(payload);

            if (err < 0) {
                ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                break;
            }
            ESP_LOGI(TAG, "Message sent");

            vTaskDelay(2000 / portTICK_PERIOD_MS); // ayuda para problemas de conexión. Limpiar variables en el puerto en el que se recibe con un print
        }
    }

}

void tcp_client(char protocol) {
    char rx_buffer[128];
    char host_ip[] = HOST_IP_ADDR;
    int addr_family = 0;
    int ip_protocol = 0;

    while (1) {
#if defined(CONFIG_EXAMPLE_IPV4)
        struct sockaddr_in dest_addr;
        inet_pton(AF_INET, host_ip, &dest_addr.sin_addr);
        dest_addr.sin_family = AF_INET;
        dest_addr.sin_port = htons(PORT + 2);
        addr_family = AF_INET;
        ip_protocol = IPPROTO_IP;
#elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
        struct sockaddr_storage dest_addr = { 0 };
        ESP_ERROR_CHECK(get_addr_from_stdin(PORT + 2, SOCK_STREAM, &ip_protocol, &addr_family, &dest_addr));
#endif
        int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
        if (sock < 0) {
            ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
            break;
        }
        ESP_LOGI(TAG, "Socket created, connecting to %s:%d", host_ip, PORT + 2);

        int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
        if (err != 0) {
            ESP_LOGE(TAG, "Socket unable to connect: errno %d", errno);
            break;
        }
        ESP_LOGI(TAG, "Successfully connected");
        while (1) {
            char* payload = malloc(messageLength(protocol));
            char* header = malloc(12);
            char* message;

            int int_protocol = (int)protocol - 48;

            switch (int_protocol) {
                case 1:
                    message = dataprotocol1(header);
                    break;
                case 2:
                    message = dataprotocol2(header);
                    break;
                case 3:
                    message = dataprotocol3(header);
                    break;
                case 4:
                    message = dataprotocol4(header);
                    break;
                case 5:
                    message = dataprotocol4(header);
                    break;
                default:
                    message = dataprotocol1(header);
                    break;
            }
            memcpy((void*)&(payload[0]), (void*)header, 12);
            memcpy((void*)&(payload[12]), (void*)message, dataLength(int_protocol));
            free(header);
            free(message);

            ESP_LOGI(TAG, "largo del mensaje: %d", messageLength(int_protocol));
            err = send(sock, payload, messageLength(int_protocol), 0); // mando mensaje de saludo por TCP
            free(payload);

            if (err < 0) {
                ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
                break;
            }

            int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
            // Error occurred during receiving
            if (len < 0) {
                ESP_LOGE(TAG, "recv failed: errno %d", errno);
                break;
            }
            // Data received
            else if (rx_buffer[0] != 1) {
                ESP_LOGE(TAG, "recv failed: OK value is not 1");
                break;
            }
            else {
                rx_buffer[len] = 0; // Null-terminate whatever we received and treat like a string

                ESP_LOGI(TAG, "Received %d bytes from %s:", len, host_ip);
                ESP_LOGI(TAG, "%s", rx_buffer);
                esp_sleep_enable_timer_wakeup(60*1000000);

                shutdown(sock, 0);
                close(sock);
                esp_deep_sleep_start();
            }
        }


        if (sock != -1) {
            ESP_LOGE(TAG, "Shutting down socket and restarting...");
            shutdown(sock, 0);
            close(sock);
        }
    }
}

void tcp_config_socket(void) {
    char rx_buffer[128];
    char host_ip[] = HOST_IP_ADDR;
    int addr_family = 0;
    int ip_protocol = 0;

#if defined(CONFIG_EXAMPLE_IPV4)
    struct sockaddr_in dest_addr;
    inet_pton(AF_INET, host_ip, &dest_addr.sin_addr);
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(PORT);
    addr_family = AF_INET;
    ip_protocol = IPPROTO_IP;
#elif defined(CONFIG_EXAMPLE_SOCKET_IP_INPUT_STDIN)
    struct sockaddr_storage dest_addr = { 0 };
    ESP_ERROR_CHECK(get_addr_from_stdin(PORT, SOCK_STREAM, &ip_protocol, &addr_family, &dest_addr));
#endif
    int sock =  socket(addr_family, SOCK_STREAM, ip_protocol);
    if (sock < 0) {
        ESP_LOGE(TAG, "Unable to create socket: errno %d", errno);
        return;
    }
    ESP_LOGI(TAG, "Socket created, connecting to %s:%d", host_ip, PORT);

    int err = connect(sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
    if (err != 0) {
        ESP_LOGE(TAG, "Socket unable to connect: errno %d", errno);
        return;
    }
    ESP_LOGI(TAG, "Successfully connected");

    // MENSAJE DE SALUDO

    char* saludo = "\0";
    ESP_LOGI(TAG, "Enviando mensaje de saludo...");
    err = send(sock, saludo, 1, 0);
    if (err < 0) {
        ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
        return;
    }
    ESP_LOGI(TAG, "Mensaje de saludo enviado");

    int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
    if (len < 0) {
        ESP_LOGE(TAG, "recv failed: errno %d", errno);
        return;
    }
    ESP_LOGI(TAG, "Configuración recibida");
    rx_buffer[len] = 0;
    char protocol =  rx_buffer[0];
    char transport_layer = rx_buffer[1];

    shutdown(sock, 0);
    close(sock);
    ESP_LOGI(TAG, "Protocol: %d", protocol);
    ESP_LOGI(TAG, "Transport layer: %d", transport_layer);

    if (transport_layer == '0') {
        ESP_LOGI(TAG, "llamando TCP client");
        tcp_client(protocol);
    }
    else {
        ESP_LOGI(TAG, "llamando UDP client");
        udp_client(protocol);
    }
}
