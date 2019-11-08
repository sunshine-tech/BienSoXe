========
BienSoXe
========

Library to validate and parse Vietnamese vehicle plate.

This library is not a computer-vision-based license plate recognition software. It instead is used for validating output of such computer vision software. Imagine that you use camera to track all cars coming in and out of your parking lot, but you don't want to save false data generated from recognition process (due to wrong angle of canera, for example).

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

Django
~~~~~~

This library provides a field type, ``VietnamVehiclePlateField``, for Django model. The field will return value as ``VietnamVehiclePlate`` object. Here is example:

.. code-block:: python

    from biensoxe.django import VietnamVehiclePlateField

    def default_plate_number():
        return VietnamVehiclePlate.from_string('10A 00001')

    class Vehicle(models.Model):
        plate_number = VietnamVehiclePlateField(max_length=20, default=default_plate_number, unique=True)

    def __str__(self):
        return str(self.plate_number) or self.pk

Note that this field stores value internally as PostgeSQL ``CIText`` data type, so you can only use this field with PostgreSQL.
You also need to activate CITextExtension_ your self.


.. _CITextExtension: https://docs.djangoproject.com/en/2.2/ref/contrib/postgres/operations/#citextextension
