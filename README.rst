========
BienSoXe
========

Library to parse and validate Vietnamese vehicle plate

Install
-------

.. code-block:: sh

    pip3 install biensoxe


Usage
-----

Call ``VietnamVehiclePlate.from_string``, passing the number string, to create ``VietnamVehiclePlate`` object.

.. code-block:: python

    >>> from biensoxe import VietnamVehiclePlate

    >>> VietnamVehiclePlate.from_string('44A-112.23')
    VietnamVehiclePlate(compact='44A11223', vehicle_type=<VehicleType.DOMESTIC_AUTOMOBILE: 1>,
    series='A', order='11223', locality='44', dip_country=None)

The method raises ``ValueError`` if the string could not be parsed.

To format the plate number as in daily life, pass ``VietnamVehiclePlate`` to ``str``:

.. code-block:: python

    >>> plate = VietnamVehiclePlate.from_string('72E101130')

    >>> plate
    VietnamVehiclePlate(compact='72E101130', vehicle_type=<VehicleType.DOMESTIC_MOTORCYCLE_50_TO_175CC: 3>, series='E1', order='01130', locality='72', dip_country=None)

    >>> str(plate)
    '72-E1 011.30'
