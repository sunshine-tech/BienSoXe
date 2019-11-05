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

.. code-block:: python

    >>> from biensoxe import VietnamVehiclePlate

    >>> VietnamVehiclePlate.from_string('44A-112.23')
    VietnamVehiclePlate(compact='44A11223', vehicle_type=<VehicleType.DOMESTIC_AUTOMOBILE: 1>,
    series='A', order='11223', locality='44', dip_country=None)
