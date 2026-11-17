#include "ia1_control.h"

#include <math.h>

static int finite_value(float value)
{
    return isfinite(value) != 0;
}

void ia1_control_init(Ia1Control *control, const Ia1Config *config)
{
    if (control == NULL || config == NULL) {
        return;
    }
    control->config = *config;
    control->mode = IA1_MODE_AUTO;
    control->status = IA1_ENV_NORMAL;
    control->fanOn = 0;
    control->lightOn = 0;
}

void ia1_control_apply_command(Ia1Control *control, Ia1Command command)
{
    if (control == NULL) {
        return;
    }
    switch (command) {
        case IA1_COMMAND_AUTO:
            control->mode = IA1_MODE_AUTO;
            break;
        case IA1_COMMAND_FAN_ON:
            control->mode = IA1_MODE_MANUAL;
            control->fanOn = 1;
            break;
        case IA1_COMMAND_FAN_OFF:
            control->mode = IA1_MODE_MANUAL;
            control->fanOn = 0;
            break;
        case IA1_COMMAND_LIGHT_ON:
            control->mode = IA1_MODE_MANUAL;
            control->lightOn = 1;
            break;
        case IA1_COMMAND_LIGHT_OFF:
            control->mode = IA1_MODE_MANUAL;
            control->lightOn = 0;
            break;
        default:
            break;
    }
}

void ia1_control_step(Ia1Control *control, float temperature, float humidity, float lux)
{
    if (control == NULL) {
        return;
    }
    if (!finite_value(temperature) || !finite_value(humidity) || !finite_value(lux)) {
        control->status = IA1_ENV_FAULT;
        return;
    }

    if (control->mode == IA1_MODE_AUTO) {
        if (control->lightOn) {
            if (lux > control->config.luxHigh) {
                control->lightOn = 0;
            }
        } else if (lux < control->config.luxLow) {
            control->lightOn = 1;
        }

        if (control->fanOn) {
            if (temperature < control->config.temperatureLow && humidity < control->config.humidityLow) {
                control->fanOn = 0;
            }
        } else if (temperature > control->config.temperatureHigh || humidity > control->config.humidityHigh) {
            control->fanOn = 1;
        }
    }

    if (temperature > control->config.temperatureHigh || humidity > control->config.humidityHigh || lux < control->config.luxLow) {
        control->status = IA1_ENV_ABNORMAL;
    } else if (temperature > control->config.temperatureHigh - 2.0f || humidity > control->config.humidityHigh - 5.0f) {
        control->status = IA1_ENV_WARNING;
    } else {
        control->status = IA1_ENV_NORMAL;
    }
}

const char *ia1_status_name(Ia1EnvironmentStatus status)
{
    switch (status) {
        case IA1_ENV_NORMAL: return "normal";
        case IA1_ENV_WARNING: return "warning";
        case IA1_ENV_ABNORMAL: return "abnormal";
        case IA1_ENV_FAULT: return "fault";
        default: return "unknown";
    }
}


