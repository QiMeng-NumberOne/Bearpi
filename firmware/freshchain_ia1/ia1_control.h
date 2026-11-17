#ifndef FRESHCHAIN_IA1_CONTROL_H
#define FRESHCHAIN_IA1_CONTROL_H

#include <stddef.h>

typedef enum {
    IA1_MODE_AUTO = 0,
    IA1_MODE_MANUAL = 1
} Ia1Mode;

typedef enum {
    IA1_ENV_NORMAL = 0,
    IA1_ENV_WARNING = 1,
    IA1_ENV_ABNORMAL = 2,
    IA1_ENV_FAULT = 3
} Ia1EnvironmentStatus;

typedef struct {
    float luxLow;
    float luxHigh;
    float temperatureLow;
    float temperatureHigh;
    float humidityLow;
    float humidityHigh;
} Ia1Config;

typedef struct {
    Ia1Config config;
    Ia1Mode mode;
    Ia1EnvironmentStatus status;
    unsigned char fanOn;
    unsigned char lightOn;
} Ia1Control;

typedef enum {
    IA1_COMMAND_AUTO = 0,
    IA1_COMMAND_FAN_ON = 1,
    IA1_COMMAND_FAN_OFF = 2,
    IA1_COMMAND_LIGHT_ON = 3,
    IA1_COMMAND_LIGHT_OFF = 4
} Ia1Command;

void ia1_control_init(Ia1Control *control, const Ia1Config *config);
void ia1_control_step(Ia1Control *control, float temperature, float humidity, float lux);
void ia1_control_apply_command(Ia1Control *control, Ia1Command command);
const char *ia1_status_name(Ia1EnvironmentStatus status);

#endif


