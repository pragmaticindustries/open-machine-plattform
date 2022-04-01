MQTT Data-Exchange Format
=========================

OMAP uses `MQTT <https://de.wikipedia.org/wiki/MQTT>`_ as telemetry endpoint.
But we distinguish between MQTT in general, which is the transport layer and a specific payload and topic structure that is used to parse the messages and distribute them to the according apps / modules to be handled.
This part of the documentation describes the respective topics and the expected payload formats that are used in the core modules of the OMAP.

General Considerations
----------------------

Currently, all endpoints use the JSON format for the payload. In the future there may be more efficient formats but for now JSON encoding is the standard.
If not stated otherwise, all timestamps are meant as the timestamps that the respective event occured or the measurement was taken. Furthermore, timestamps are generally transmitted as `epoch millis <https://en.wikipedia.org/wiki/Unix_time>`_, i.e. the milliseconds passed since 1.1.1970 00:00 in UTC.
Furthermore, the messages / topics contain a *device id* which is a unique identifier provided by the OMAP instance.

.. note:: We use Access Control on all topics. So devices may only be able to send data on "their" topics and not even able to read there. So do not wonder.

An example message could look like follows

.. code-block:: json

    {
        "timestamp": 1638359202000,
        "device_id": "7e40e8400-e29b-11d4-4716-44665544f2de",
        "data": {
            "current_01": 12.21,
            "current_02": 125.1,
            "voltage_01": 24.2,
            "voltage_02": 24.05
        }
    }


General Topic Structure
-----------------------

The core apps all use a similar topic structure which is

.. code-block::

    <request_type>/<api_version>/<tenant_id>/<device_id>/<app>

where the elements are

* request_type
    tbd
* api_version
    tbd
* tenant_id
    tbd
* device_id
    tbd
* app
    tbd

