----------------
OpenPolitici API
----------------

Institutions
************

Resource URI
++++++++++++

::

    GET /politici/v2/istituzioni/{id}

Resource Properties
+++++++++++++++++++

A InstitutionalCharge is identified by the following properties:

============================= ==========================================================
property                      explanation
============================= ==========================================================
:const:`id`                   openpolis Institution identifier
:const:`name`                 name of institution
:const:`rappresentanti_uri`   uri to filter rappresentanti by Institution
============================= ==========================================================



Politician
**********

Resource URI
++++++++++++

::

    GET /politici/v2/politici/{id}

Resource Properties
+++++++++++++++++++

A Politician is identified by the following properties:

=============================== ==========================================================
property                        explanation
=============================== ==========================================================
:const:`birth_date`             birth date
:const:`birth_location`         birth location
:const:`death_date`             date of death or null
:const:`education_levels`       array of name and description education levels
:const:`first_name`             first name
:const:`institution_charges`    array of :ref:`institution-charges`
:const:`last_charge_update`     latest charge date
:const:`last_name`              last name
:const:`minint_aka`
:const:`organization_charges`   array of :ref:`organization-charges`
:const:`political_charges`      array of :ref:`political-charges`
:const:`profession`             profession name and description
:const:`resource_uri`           politician uri
:const:`resources`              array of :ref:`resources`
:const:`sex`                    M or F
=============================== ==========================================================

*Filters* : TODO

.. note::
  :const:`education_levels`, :const:`institution_charges`, :const:`organization_charges`, :ref:`resources`
  and :const:`political_charges` are array of resource_uri on list request (aka index);
  full info is provided on detail request

InstitutionalCharges
********************

Every Politician may has many InstitutionalCharges, representing their appointment at a Institution.

Resource URI
++++++++++++

::

    GET /politici/v2/cariche_istituzionali/{id}


Resource Properties
+++++++++++++++++++

A InstitutionalCharge is identified by the following properties:

============================= ==========================================================
property                      explanation
============================= ==========================================================
:const:`id`                   openpolis identifier
:const:`charge_type`          :ref:`charge_type`
:const:`date_start`           charge start date (yyyy-mm-dd)
:const:`date_end`             charge end date (yyyy-mm-dd)
:const:`description`          charge description ( not used yet, see textual_rep below )
:const:`group`                group (if parliament, regional)
:const:`institution`          :ref:`institution`
:const:`location_name`        location name
:const:`location_id`          location id
:const:`location`             location uri
:const:`minint_verified_at`   date of last institutional charge check
:const:`party`                party of election
:const:`politician`           :ref:`politician`
:const:`resource_uri`         uri of institutional charge
:const:`textual_rep`          description of institutional charge
============================= ==========================================================

*Filters* : 'date_end', 'location', 'charge_type'

.. note::
  :const:`location` contains resource_uri to location; full info is provided on detail request

PoliticalChargeResource
***********************

Resource URI
++++++++++++

::

    /politici/v2/cariche_politiche/{id}


Resource Properties
+++++++++++++++++++

A PoliticalChargeResource is identified by the following properties:

============================= ==========================================================
property                      explanation
============================= ==========================================================
:const:`id`                   openpolis identifier
:const:`date_start`           charge start date (yyyy-mm-dd)
:const:`date_end`             charge end date (yyyy-mm-dd)
:const:`description`          charge description ( not used yet, see textual_rep below )
:const:`location_name`        location name
:const:`location_id`          location id
:const:`location`             location uri
:const:`party`                party of election
:const:`politician`           :ref:`politician`
:const:`resource_uri`         uri of institutional charge
:const:`textual_rep`          description of institutional charge
============================= ==========================================================

*Filters* : 'date_end', 'location', 'charge_type'

.. note::
  :const:`location` contains resource_uri to location; full info is provided on detail request


OrganizationChargeResource
**************************

Resource URI
++++++++++++

::

    /politici/v2/cariche_organizzazioni/{id}


Resource Properties
+++++++++++++++++++

A OrganizationChargeResource is identified by the following properties:

============================= ==========================================================
property                      explanation
============================= ==========================================================
:const:`id`                   openpolis identifier
:const:`charge_name`          charge's name of organization
:const:`current`              is currently in charge
:const:`date_start`           charge start date (yyyy-mm-dd)
:const:`date_end`             charge end date (yyyy-mm-dd)
:const:`politician`           :ref:`politician`
:const:`resource_uri`         uri of institutional charge
:const:`textual_rep`          description of institutional charge
============================= ==========================================================

*Filters* : 'date_end', 'charge_name'



DeputiesResource
****************

Display politician with a charge now!

Resource URI
++++++++++++

::

    GET /politici/v2/rappresentanti/

Resource Properties
+++++++++++++++++++


============================= ==========================================================
property                      explanation
============================= ==========================================================
:const:`birth_date`             birth date
:const:`birth_location`         birth location
:const:`death_date`             date of death (only if exists)
:const:`first_name`             first name
:const:`full_name`              first name + last name
:const:`institution_charges`    array of :ref:`institution-charges`
:const:`last_charge_update`     latest charge date
:const:`last_name`              last name
:const:`minint_aka`
:const:`resource_uri`           politician uri
:const:`sex`                    M or F
============================= ==========================================================

Filters
^^^^^^^
::

    data : 'all' or 'YYYY-MM-DD'
    territorio: id of Location ( only Cities )
    istituzione: id of Institution
    tipo_carica: id of ChargeType

    birth_date: ALL
    sex: 'M' or 'F'
    last_name: ALL
    first_name: ALL
    death_date: ALL

.. note::
  filter by territorio shows all Politician with a InstitutionCharge related to it.
  ( Comune + Provincia + Regione + parti di Camera, Senato e Parlamento europeo + Commissione Europea )
  BOTTOM UP
