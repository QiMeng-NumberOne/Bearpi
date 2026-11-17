#ifndef FRESHCHAIN_ST1_TRACKER_H
#define FRESHCHAIN_ST1_TRACKER_H

typedef enum {
    ST1_STATUS_GPS_SEARCHING = 0,
    ST1_STATUS_IN_ZONE = 1,
    ST1_STATUS_IN_TRANSIT = 2,
    ST1_STATUS_OUT_OF_ZONE = 3,
    ST1_STATUS_DELIVERED = 4
} St1Status;

typedef enum {
    ST1_COMMAND_START_TRANSPORT = 0,
    ST1_COMMAND_END_TRANSPORT = 1,
    ST1_COMMAND_SILENCE = 2
} St1Command;

typedef struct {
    double latitude;
    double longitude;
    double radiusMeters;
    unsigned char geofenceReady;
    unsigned char transportStarted;
    unsigned char alarmLatched;
    unsigned char buzzerEnabled;
    St1Status status;
    double lastLatitude;
    double lastLongitude;
} St1Tracker;

void st1_tracker_init(St1Tracker *tracker);
void st1_tracker_set_geofence(St1Tracker *tracker, double latitude, double longitude, double radiusMeters);
void st1_tracker_apply_command(St1Tracker *tracker, St1Command command);
void st1_tracker_step(St1Tracker *tracker, unsigned char gpsValid, double latitude, double longitude);
double st1_distance_m(double latitude1, double longitude1, double latitude2, double longitude2);
const char *st1_status_name(St1Status status);

#endif


