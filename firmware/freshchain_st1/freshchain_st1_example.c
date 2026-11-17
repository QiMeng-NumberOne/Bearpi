/* FreshChain ST1 node for BearPi-HM Nano. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "ohos_init.h"
#include "cmsis_os2.h"
#include "wifi_connect.h"
#include "MQTTClient.h"
#include "E53_ST1.h"

#include "st1_tracker.h"

#define FRESHCHAIN_WIFI_SSID "QiMeng"
#define FRESHCHAIN_WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
#define FRESHCHAIN_MQTT_HOST "YOUR_PC_IP"
#define FRESHCHAIN_MQTT_PORT 1884
#define FRESHCHAIN_CLIENT_ID "freshchain-st1"
#define FRESHCHAIN_TELEMETRY_TOPIC "freshchain/st1/telemetry"
#define FRESHCHAIN_COMMAND_TOPIC "freshchain/st1/command"

static Network g_network;
static MQTTClient g_client;
static unsigned char g_send_buffer[1024];
static unsigned char g_read_buffer[1024];
static St1Tracker g_tracker;
static volatile int g_mqtt_connected;
static volatile int g_has_command;
static volatile St1Command g_pending_command;
static volatile double g_pending_latitude;
static volatile double g_pending_longitude;
static volatile double g_pending_radius;

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

static double json_number(const char *payload, const char *key, double fallback)
{
    const char *start;
    char *end;
    if (payload == NULL || key == NULL) {
        return fallback;
    }
    start = strstr(payload, key);
    if (start == NULL) {
        return fallback;
    }
    start = strchr(start, ':');
    if (start == NULL) {
        return fallback;
    }
    start++;
    while (*start == ' ' || *start == '\t') {
        start++;
    }
    double value = strtod(start, &end);
    return end == start ? fallback : value;
}

static void freshchain_st1_message_arrived(MessageData *data)
{
    char payload[220];
    char compact[220];
    int length;

    if (data == NULL || data->message == NULL) {
        return;
    }
    length = data->message->payloadlen;
    if (length >= (int)sizeof(payload)) {
        length = (int)sizeof(payload) - 1;
    }
    memcpy(payload, data->message->payload, (size_t)length);
    payload[length] = '\0';
    json_compact(payload, compact, sizeof(compact));

    if (json_has(compact, "\"action\":\"start_transport\"")) {
        g_pending_command = ST1_COMMAND_START_TRANSPORT;
        g_has_command = 1;
    } else if (json_has(compact, "\"action\":\"end_transport\"")) {
        g_pending_command = ST1_COMMAND_END_TRANSPORT;
        g_has_command = 1;
    } else if (json_has(compact, "\"action\":\"silence\"")) {
        g_pending_command = ST1_COMMAND_SILENCE;
        g_has_command = 1;
    } else if (json_has(compact, "\"action\":\"set_geofence\"")) {
        g_pending_latitude = json_number(compact, "\"latitude\"", g_tracker.latitude);
        g_pending_longitude = json_number(compact, "\"longitude\"", g_tracker.longitude);
        g_pending_radius = json_number(compact, "\"radius_m\"", g_tracker.radiusMeters);
        st1_tracker_set_geofence(&g_tracker, g_pending_latitude, g_pending_longitude, g_pending_radius);
    }
}

static int freshchain_st1_mqtt_connect(void)
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
    rc = MQTTSubscribe(&g_client, FRESHCHAIN_COMMAND_TOPIC, 0, freshchain_st1_message_arrived);
    if (rc != 0) {
        MQTTDisconnect(&g_client);
        NetworkDisconnect(&g_network);
        return rc;
    }
    g_mqtt_connected = 1;
    return 0;
}

static int freshchain_st1_publish(const E53_ST1_Data_TypeDef *data, unsigned char gps_valid)
{
    MQTTMessage message;
    char payload[320];
    int length;

    length = snprintf(payload, sizeof(payload),
        "{\"node\":\"st1\",\"gps_valid\":%d,\"latitude\":%.6f,\"longitude\":%.6f,"
        "\"speed\":0.0,\"zone_status\":\"%s\",\"alarm\":%d,\"buzzer\":%d,"
        "\"transport_status\":\"%s\"}",
        gps_valid, data->Latitude, data->Longitude, st1_status_name(g_tracker.status),
        g_tracker.alarmLatched, g_tracker.alarmLatched && g_tracker.buzzerEnabled,
        g_tracker.transportStarted ? "in_transit" : "ready");
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

static void freshchain_st1_task(void)
{
    E53_ST1_Data_TypeDef data = {0};
    unsigned char gps_valid;
    unsigned int sample_elapsed_ms = 5000;

    st1_tracker_init(&g_tracker);
    Init_E53_ST1();
    WifiConnect(FRESHCHAIN_WIFI_SSID, FRESHCHAIN_WIFI_PASSWORD);

    while (1) {
        if (!g_mqtt_connected) {
            if (freshchain_st1_mqtt_connect() != 0) {
                osDelay(2000);
                continue;
            }
        }
        (void)MQTTYield(&g_client, 100);
        if (g_has_command) {
            st1_tracker_apply_command(&g_tracker, g_pending_command);
            g_has_command = 0;
        }
        if (sample_elapsed_ms >= 5000) {
            E53_ST1_Read_Data(&data);
            gps_valid = data.Valid ? 1 : 0;
            st1_tracker_step(&g_tracker, gps_valid, data.Latitude, data.Longitude);
            Beep_StatusSet(g_tracker.alarmLatched && g_tracker.buzzerEnabled ? ON : OFF);
            if (freshchain_st1_publish(&data, gps_valid) != 0) {
                g_mqtt_connected = 0;
                MQTTDisconnect(&g_client);
                NetworkDisconnect(&g_network);
                continue;
            }
            sample_elapsed_ms = 0;
        }
        osDelay(100);
        sample_elapsed_ms += 100;
    }
}

static void FreshChainSt1App(void)
{
    osThreadAttr_t attr = {
        .name = "freshchain_st1",
        .stack_size = 8192,
        .priority = osPriorityNormal,
    };
    if (osThreadNew((osThreadFunc_t)freshchain_st1_task, NULL, &attr) == NULL) {
        printf("FreshChain ST1 task creation failed\n");
    }
}

APP_FEATURE_INIT(FreshChainSt1App);


