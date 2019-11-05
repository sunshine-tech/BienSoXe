import pytest

from biensoxe import VietnamVehiclePlate, VehicleType
from biensoxe.core import REGEXES

automobile_data = (
    ('29A 433.74', '29', 'A'),
    ('51G99999', '51', 'G'),
    ('30F24420', '30', 'F'),
    # Old
    ('30S5555', '30', 'S'),
    ('33M3456', '33', 'M'),
    ('31F6789', '31', 'F'),
    ('14P 2222', '14', 'P'),
    ('29X 9999', '29', 'X'),
    ('30H 4444', '30', 'H'),
    ('30Y 9999', '30', 'Y')
)

low_capacity_motorcycle_data = (
    ('50HA 6666', '50', 'HA'),
    ('75FB 6666', '75', 'FB'),
    ('63AN 00419', '63', 'AN'),
)

medium_capacity_motorcycle_data = (
    ('68G166886', '68', 'G1'),
    ('29F3 9999', '29', 'F3'),
    ('29L5 9999', '29', 'L5'),
    ('66V1 34567', '66', 'V1'),
    ('51U3 6119', '51', 'U3'),
)

high_capacity_motorcycle_data = (
    ('43A1 000.52', '43', 'A1'),
)

electrical_motorcycle_data = (
    ('29MĐ1 94190', '29', 'MĐ1'),
)


@pytest.mark.parametrize("original_string, locality, series", automobile_data)
def test_automobile(original_string, locality, series):
    print(REGEXES[VehicleType.DOMESTIC_AUTOMOBILE])
    plate = VietnamVehiclePlate.from_string(original_string)
    assert plate.vehicle_type == VehicleType.DOMESTIC_AUTOMOBILE
    assert plate.locality == locality
    assert plate.series == series


@pytest.mark.parametrize("original_string, locality, series", low_capacity_motorcycle_data)
def test_low_capacity_motorcycle(original_string, locality, series):
    plate = VietnamVehiclePlate.from_string(original_string)
    assert plate.vehicle_type == VehicleType.DOMESTIC_MOTORCYCLE_UNDER_50CC
    assert plate.locality == locality
    assert plate.series == series


@pytest.mark.parametrize("original_string, locality, series", electrical_motorcycle_data)
def test_electrical_motorcycle_data(original_string, locality, series):
    plate = VietnamVehiclePlate.from_string(original_string)
    assert plate.vehicle_type == VehicleType.NON_BUSINESS_SPECIAL
    assert plate.locality == locality
    assert plate.series == series


@pytest.mark.parametrize("original_string, locality, series", high_capacity_motorcycle_data)
def test_high_capacity_motorcycle(original_string, locality, series):
    plate = VietnamVehiclePlate.from_string(original_string)
    assert plate.vehicle_type == VehicleType.DOMESTIC_MOTORCYCLE_OVER_175CC
    assert plate.locality == locality
    assert plate.series == series


def test_invalid_plate_number():
    with pytest.raises(ValueError):
        VietnamVehiclePlate.from_string('XXYYZZ11')
