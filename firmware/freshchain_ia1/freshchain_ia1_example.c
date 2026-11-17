/*
 * FreshChain IA1 node for BearPi-HM Nano.
 *
 * Copy this file and the business-logic files into a BearPi-HM Nano
 * OpenHarmony sample.  The E53 driver API matches the official D12
 * agriculture sample; the MQTT API matches the official D5 sample.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "ohos_init.h"
#include "cmsis_os2.h"
#include "wifi_connect.h"
#include "MQTTClient.h"
#include "E53_IA1.h"

#include "ia1_control.h"

#define FRESHCHAIN_WIFI_SSID "QiMeng"
#define FRESHCHAIN_WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define FRESHCHAIN_MQTT_HOST "YOUR_PC_IP" /* laptop LAN address */
#define FRESHCHAIN_MQTT_PORT 1884
#define FRESHCHAIN_CLIENT_ID "freshchain-ia1"
#define FRESHCHAIN_TELEMETRY_TOPIC "freshchain/ia1/telemetry"
#define FRESHCHAIN_COMMAND_TOPIC "freshchain/ia1/command"
#define FRESHCHAIN_SAMPLE_SECONDS 1

static Network g_network;
static MQTTClient g_client;
static unsigned char g_send_buffer[1024];
static unsigned char g_read_buffer[1024];
static Ia1Control g_control;
static volatile int g_mqtt_connected;
static volatile int g_has_command;
static volatile Ia1Command g_pending_command;

static int json_has(const char *payload, const char *needle)
{
    return payload != NULL && needle != NULL && strstr(payload, needle) != NULL;
}

/* Accept both compact and pretty-printed JSON from the gateway. */
static void json_compact(const char *src, char *dst, size_t dst_size)
{
    size_t i;
    size_t j = 0;
    int in_string = 0;
    int escaped = 0;

    if (dst_size == 0) {
        return;
    }
    for (i = 0; src != NULL && src[i] != '\0' && j + 1 < dst_size; i++) {
        char c = src[i];
        if (escaped) {
            dst[j++] = c;
            escaped = 0;
        } else if (in_string && c == '\\') {
            dst[j++] = c;
            escaped = 1;
        } else if (c == '"') {
            in_string = !in_string;
            dst[j++] = c;
        } else if (!in_string && (c == ' ' || c == '\t' || c == '\r' || c == '\n')) {
            continue;
        } else {
            dst[j++] = c;
        }
    }
    dst[j] = '\0';
}

static void freshchain_ia1_message_arrived(MessageData *data)
{
    char payload[160];
    char compact[160];
    int length;

    if (data == NULL || data->message == NULL) {
        return;
    }
    length = data->message->payloadlen;
    if (length < 0) {
        return;
    }
    if (length >= (int)sizeof(payload)) {
        length = (int)sizeof(payload) - 1;
    }
    memcpy(payload, data->message->payload, (size_t)length);
    payload[length] = '\0';
    json_compact(payload, compact, sizeof(compact));

    if (json_has(compact, "\"action\":\"set_mode\"") && json_has(compact, "\"mode\":\"auto\"")) {
        g_pending_command = IA1_COMMAND_AUTO;
        g_has_command = 1;
    } else if (json_has(compact, "\"action\":\"fan\"") && json_has(compact, "\"value\":1")) {
        g_pending_command = IA1_COMMAND_FAN_ON;
        g_has_command = 1;
    } else if (json_has(compact, "\"action\":\"fan\"") && json_has(compact, "\"value\":0")) {
        g_pending_command = IA1_COMMAND_FAN_OFF;
        g_has_command = 1;
    } else if (json_has(compact, "\"action\":\"light\"") && json_has(compact, "\"value\":1")) {
        g_pending_command = IA1_COMMAND_LIGHT_ON;
        g_has_command = 1;
    } else if (json_has(compact, "\"action\":\"light\"") && json_has(compact, "\"value\":0")) {
        g_pending_command = IA1_COMMAND_LIGHT_OFF;
        g_has_command = 1;
    }
}

static int freshchain_ia1_mqtt_connect(void)
{
    MQTTPacket_connectData connect_data = MQTTPacket_connectData_initializer;
    MQTTString client_id = MQTTString_initializer;
    int rc;

    NetworkInit(&g_network);
    rc = NetworkConnect(&g_network, FRESHCHAIN_MQTT_HOST, FRESHCHAIN_MQTT_PORT);
    if (rc != 0) {
        return rc;
    }
    MQTTClientInit(&g_client, &g_network, 2000, g_send_buffer, sizeof(g_send_buffer), g_read_buffer, sizeof(g_read_buffer));
    client_id.cstring = FRESHCHAIN_CLIENT_ID;
    connect_data.clientID = client_id;
    connect_data.MQTTVersion = 3;
    connect_data.keepAliveInterval = 60;
    connect_data.cleansession = 1;
    rc = MQTTConnect(&g_client, &connect_data);
    if (rc != 0) {
        NetworkDisconnect(&g_network);
        return rc;
    }
    rc = MQTTSubscribe(&g_client, FRESHCHAIN_COMMAND_TOPIC, 0, freshchain_ia1_message_arrived);
    if (rc != 0) {
        MQTTDisconnect(&g_client);
        NetworkDisconnect(&g_network);
        return rc;
    }
    g_mqtt_connected = 1;
    return 0;
}

static int freshchain_ia1_publish(const E53_IA1_Data_TypeDef *data)
{
    MQTTMessage message;
    char payload[320];
    int length;

    length = snprintf(payload, sizeof(payload),
        "{\"node\":\"ia1\",\"temperature\":%.2f,\"humidity\":%.2f,\"lux\":%.2f,"
        "\"fan\":%d,\"light\":%d,\"mode\":\"%s\",\"environment_status\":\"%s\"}",
        data->Temperature, data->Humidity, data->Lux,
        g_control.fanOn, g_control.lightOn,
        g_control.mode == IA1_MODE_AUTO ? "auto" : "manual",
        ia1_status_name(g_control.status));
    if (length <= 0 || length >= (int)sizeof(payload)) {
        return -1;
    }
    memset(&message, 0, sizeof(message));
    message.qos = 0;
    message.retained = 0;
    message.payload = payload;
    message.payloadlen = (size_t)length;
    return MQTTPublish(&g_client, FRESHCHAIN_TELEMETRY_TOPIC, &message);
}

static void freshchain_ia1_apply_outputs(void)
{
    Motor_StatusSet(g_control.fanOn ? ON : OFF);
    Light_StatusSet(g_control.lightOn ? ON : OFF);
}

static void freshchain_ia1_task(void)
{
    E53_IA1_Data_TypeDef data = {0};
    uint32_t sample_period_ticks;
    uint32_t last_sample_ticks;
    Ia1Config config = {
        .luxLow = 20.0f,
        .luxHigh = 40.0f,
        .temperatureLow = 24.0f,
        .temperatureHigh = 30.0f,
        .humidityLow = 65.0f,
        .humidityHigh = 75.0f,
    };

    E53_IA1_Init();
    ia1_control_init(&g_control, &config);
    freshchain_ia1_apply_outputs();
    WifiConnect(FRESHCHAIN_WIFI_SSID, FRESHCHAIN_WIFI_PASSWORD);

    sample_period_ticks = osKernelGetTickFreq() * FRESHCHAIN_SAMPLE_SECONDS;
    last_sample_ticks = osKernelGetTickCount() - sample_period_ticks;

    while (1) {
        if (!g_mqtt_connected) {
            if (freshchain_ia1_mqtt_connect() != 0) {
                osDelay(2000);
                continue;
            }
        }

        (void)MQTTYield(&g_client, 20);
        if (g_has_command) {
            ia1_control_apply_command(&g_control, g_pending_command);
            g_has_command = 0;
            freshchain_ia1_apply_outputs();
            /* Re-evaluate auto/light immediately instead of waiting for the period. */
            last_sample_ticks = osKernelGetTickCount() - sample_period_ticks;
        }

        uint32_t now_ticks = osKernelGetTickCount();
        if ((uint32_t)(now_ticks - last_sample_ticks) >= sample_period_ticks) {
            E53_IA1_Read_Data(&data);
            ia1_control_step(&g_control, data.Temperature, data.Humidity, data.Lux);
            freshchain_ia1_apply_outputs();
            if (freshchain_ia1_publish(&data) != 0) {
                g_mqtt_connected = 0;
                MQTTDisconnect(&g_client);
                NetworkDisconnect(&g_network);
                continue;
            }
            last_sample_ticks = now_ticks;
        }
        osDelay(20);
    }
}

static void FreshChainIa1App(void)
{
    osThreadAttr_t attr = {
        .name = "freshchain_ia1",
        .stack_size = 8192,
        .priority = osPriorityNormal,
    };
    if (osThreadNew((osThreadFunc_t)freshchain_ia1_task, NULL, &attr) == NULL) {
        printf("FreshChain IA1 task creation failed\n");
    }
}

APP_FEATURE_INIT(FreshChainIa1App);


