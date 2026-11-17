#include "st1_tracker.h"

#include <stddef.h>

#define ST1_EARTH_RADIUS_M 6371000.0

static double radians(double value)
{
    return value * 0.017453292519943295;
}

static int st1_is_finite(double value)
{
    return value == value && value <= 1.0e308 && value >= -1.0e308;
}

/*
 * The Hi3861 SDK ships a reduced libm without rem_pio2/atan2.  For a small
 * geofence (tens of metres) an equirectangular approximation is accurate
 * enough and avoids pulling in the incomplete math library.
 */
static double st1_cos(double value)
{
    double x2 = value * value;
    return 1.0 - x2 / 2.0 + x2 * x2 / 24.0 - x2 * x2 * x2 / 720.0 +
           x2 * x2 * x2 * x2 / 40320.0;
}

static double st1_sqrt(double value)
{
    double root;
    int i;

    if (value <= 0.0) {
        return 0.0;
    }
    root = value > 1.0 ? value : 1.0;
    for (i = 0; i < 20; i++) {
        root = 0.5 * (root + value / root);
    }
    return root;
}

double st1_distance_m(double latitude1, double longitude1, double latitude2, double longitude2)
{
    double mean_latitude = (radians(latitude1) + radians(latitude2)) / 2.0;
    double delta_latitude = radians(latitude2 - latitude1);
    double delta_longitude = radians(longitude2 - longitude1);
    double cos_mean = st1_cos(mean_latitude);
    double x;
    double y;

    if (cos_mean < 0.0) {
        cos_mean = 0.0;
    }
    x = delta_longitude * cos_mean;
    y = delta_latitude;
    return ST1_EARTH_RADIUS_M * st1_sqrt(x * x + y * y);
}

void st1_tracker_init(St1Tracker *tracker)
{
    if (tracker == NULL) {
        return;
    }
    tracker->latitude = 0.0;
    tracker->longitude = 0.0;
    tracker->radiusMeters = 80.0;
    tracker->geofenceReady = 0;
    tracker->transportStarted = 0;
    tracker->alarmLatched = 0;
    tracker->buzzerEnabled = 1;
    tracker->status = ST1_STATUS_GPS_SEARCHING;
    tracker->lastLatitude = 0.0;
    tracker->lastLongitude = 0.0;
}

void st1_tracker_set_geofence(St1Tracker *tracker, double latitude, double longitude, double radiusMeters)
{
    if (tracker == NULL || radiusMeters <= 1.0) {
        return;
    }
    /* Reject invalid or "no fix" coordinates; otherwise a radius-only
       command would put the fence at (0,0) and alarm immediately. */
    if (!st1_is_finite(latitude) || !st1_is_finite(longitude) ||
        latitude < -90.0 || latitude > 90.0 ||
        longitude < -180.0 || longitude > 180.0 ||
        (latitude == 0.0 && longitude == 0.0)) {
        return;
    }
    tracker->latitude = latitude;
    tracker->longitude = longitude;
    tracker->radiusMeters = radiusMeters;
    tracker->geofenceReady = 1;
    tracker->alarmLatched = 0;
}

void st1_tracker_apply_command(St1Tracker *tracker, St1Command command)
{
    if (tracker == NULL) {
        return;
    }
    switch (command) {
        case ST1_COMMAND_START_TRANSPORT:
            tracker->transportStarted = 1;
            tracker->alarmLatched = 0;
            tracker->buzzerEnabled = 1;
            break;
        case ST1_COMMAND_END_TRANSPORT:
            tracker->transportStarted = 0;
            tracker->status = ST1_STATUS_DELIVERED;
            tracker->alarmLatched = 0;
            break;
        case ST1_COMMAND_SILENCE:
            tracker->buzzerEnabled = 0;
            break;
        default:
            break;
    }
}

void st1_tracker_step(St1Tracker *tracker, unsigned char gpsValid, double latitude, double longitude)
{
    if (tracker == NULL) {
        return;
    }
    if (!gpsValid || !st1_is_finite(latitude) || !st1_is_finite(longitude)) {
        tracker->status = ST1_STATUS_GPS_SEARCHING;
        return;
    }

    tracker->lastLatitude = latitude;
    tracker->lastLongitude = longitude;
    if (!tracker->geofenceReady) {
        st1_tracker_set_geofence(tracker, latitude, longitude, tracker->radiusMeters);
    }

    /* Keep the delivered state until a new transport is explicitly started. */
    if (!tracker->transportStarted && tracker->status == ST1_STATUS_DELIVERED) {
        return;
    }

    double distance = st1_distance_m(tracker->latitude, tracker->longitude, latitude, longitude);
    if (tracker->transportStarted && distance > tracker->radiusMeters) {
        tracker->status = ST1_STATUS_OUT_OF_ZONE;
        tracker->alarmLatched = 1;
    } else if (tracker->transportStarted) {
        tracker->status = ST1_STATUS_IN_TRANSIT;
    } else {
        tracker->status = ST1_STATUS_IN_ZONE;
    }
}

const char *st1_status_name(St1Status status)
{
    switch (status) {
        case ST1_STATUS_GPS_SEARCHING: return "gps_searching";
        case ST1_STATUS_IN_ZONE: return "in_zone";
        case ST1_STATUS_IN_TRANSIT: return "in_transit";
        case ST1_STATUS_OUT_OF_ZONE: return "out_of_zone";
        case ST1_STATUS_DELIVERED: return "delivered";
        default: return "unknown";
    }
}


