"""Django model field to return VietnamVehiclePlate object."""

from typing import Union, Optional

from django.db.models import Expression
from django.db.backends.postgresql.base import DatabaseWrapper
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import CICharField
from django.utils.translation import gettext_lazy as _
from biensoxe import VietnamVehiclePlate


def parse_vehicleplate(number_string: str) -> VietnamVehiclePlate:
    """Validate and parse input string to VietnamVehiclePlate object."""
    try:
        return VietnamVehiclePlate.from_string(number_string)
    except ValueError:
        raise ValidationError(_('Input string does not look like Vietname plate number'))


class VietnamVehiclePlateField(CICharField):
    """Field to store Vietnamese vehicle plate. Stored in PostgreSQL as CIText data type, to enable case-insensitive search.

    Return data as VietnamVehiclePlate type from biensoxe library.
    """

    description = _('Field to store Vietnamese vehicle plate')

    def from_db_value(self, value: Optional[str],
                      expression: Expression, connection: DatabaseWrapper):
        # Called in all circumstances when the data is loaded from the database,
        # including in aggregates and values() calls.
        if value is None:
            return value
        return parse_vehicleplate(value)

    def to_python(self, value: Union[str, VietnamVehiclePlate, None]):
        # Called by deserialization and during the clean() method used from forms.
        if isinstance(value, VietnamVehiclePlate):
            return value
        if value is None:
            return value
        return parse_vehicleplate(value)

    def get_prep_value(self, value: VietnamVehiclePlate):
        # Convert Python object back to query value
        return value.compact
