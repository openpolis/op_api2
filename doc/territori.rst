-------------
Locations API
-------------

Locations
*********

Openpolis locations are used throughout the projects in order to identify the geo-context.
It may be the constituency where a politician was elected in, or a geo-tag in an openparlamento's act,
identifying the place the act is talking about, it can be many other things.

Resource URI
++++++++++++

::

    /territori/v2/territori/

Resource Properties
*******************
A Location resource is identified by the following properties:

=============================== =======================================
property                        explanation
=============================== =======================================
:const:`id`                     openpolis identifier
:const:`name`                   location name
:const:`full_name`              full location name
:const:`macroregional_id`       macro-region identifier (istat)
:const:`regional_id`            region identifier (istat)
:const:`provincial_id`          province identifier (istat)
:const:`city_id`                city identifier (istat)
:const:`minint_regional_code`   region identifier (min. int.)
:const:`minint_provincial_code` province identifier (min. int.)
:const:`minint_city_code`       province identifier (min. int.)
:const:`gps_lat`                latitude (gps coords)
:const:`gps_lon`                longitude (gps coords)
:const:`inhabitants`            inhabitants (as of 2001)
:const:`location_type`          :ref:`location-types`
:const:`resource_uri`           Location uri
:const:`alternative_name`
:const:`new_location_id`
:const:`prov`                   name of Province if exists
:const:`last_charge_update`
:const:`rappresentanti_uri`     Optional only for city
=============================== =======================================


Type of Location
****************

Resource URI
++++++++++++

::

    /territori/v2/tipi_territori/

============================= ==========================================================
property                      explanation
============================= ==========================================================
:const:`id`                   openpolis identifier
:const:`name`                 type
:const:`territori_uri`        uri Locations filtered by type
