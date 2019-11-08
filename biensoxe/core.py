
# Author: Nguyễn Hồng Quân <ng.hong.quan@gmail.com>
#
# References:
# Legal documents: Circular 36/2010/TT-BCA, Circular 15/2014/TT-BCA
# Internet:
# https://thuvienphapluat.vn/van-ban/Giao-thong-Van-tai/Thong-tu-15-2014-TT-BCA-quy-dinh-ve-dang-ky-xe-Bo-truong-Bo-Cong-an-229224.aspx
# https://danluat.thuvienphapluat.vn/ban-da-biet-gi-ve-bien-so-xe-132978.aspx
# https://tuoitre.vn/2800-xe-bon-banh-khong-biet-xep-vao-loai-xe-gi-1078666.htm

# Note that, in this library, we only use uppercase letters

import re
import enum
from typing import Optional

from memoprop import memoized_property
from pydantic.dataclasses import dataclass

from .utils import split_to_triples


# Use this regex to strip out all illegal characters
REGEX_CLEAN_PLATE_NUMBER = re.compile(r'[^a-zđA-ZĐ0-9]')


class SpecialSeries(enum.Enum):
    DA = 'DA'  # Dự án
    KT = 'KT'  # Quân đội làm kinh tế
    LD = 'LD'  # Liên doanh


class NonBusinessSpecialSeries(enum.Enum):
    MA = 'MA'
    MĐ = 'MĐ'  # Máy điện 29-MĐ1 013.53
    MK = 'MK'  # Máy kéo
    TĐ = 'TĐ'  # Thí điểm 50TĐ-82108
    HC = 'HC'  # Hạn chế phạm vi hoạt động
    SA = 'SA'
    XA = 'XA'
    # Towed vehicles (trailers and semi-trailers)
    # https://banotore.com/xe-xe-tai-tren-10-tan-ba-ria-vung-tau/ban-tra-gop-lai-suat-thap-so-mi-ro-mooc-san-doosung-40feet3truc-aid563816
    R = 'R'   # 51R-14139


# This plate has yellow background
class SpecialEconomicZoneSeries(enum.Enum):
    LB = 'LB'  # Lao Bảo
    CT = 'CT'  # Cầu Treo
    LA = 'LA'  # Don't know where it is
    KL = 'KL'  # Don't know where it is. Found at https://www.dontu.net/2016/10/nhung-ieu-nen-biet-ve-bien-so-xe.html


class VehicleType(enum.IntEnum):
    # Appendix No 4 of Circular 15/2014/TT-BCA
    DOMESTIC_AUTOMOBILE = 1
    # https://soha.vn/xa-hoi/me-man-voi-dan-sieu-xe-bien-cuc-doc-cua-thieu-gia-dat-phu-2013050715292303.htm
    DOMESTIC_MOTORCYCLE_UNDER_50CC = enum.auto()
    DOMESTIC_MOTORCYCLE_50_TO_175CC = enum.auto()
    # https://news.zing.vn/cap-xe-phan-khoi-lon-300-trieu-bi-lam-gia-dang-ky-post631650.html
    DOMESTIC_MOTORCYCLE_OVER_175CC = enum.auto()
    # Automobiles and motorcycles used for the affiliation, project
    # and Military’s vehicles for the purpose of business
    SPECIAL_BUSINESS = enum.auto()
    SPECIAL_ECONOMIC_ZONE = enum.auto()
    # Also tractor and electrical
    NON_BUSINESS_SPECIAL = enum.auto()
    TEMPORARY = enum.auto()
    DIPLOMATIC = enum.auto()
    # Special
    MILITARY = enum.auto()


PATTERN_SPECIAL_SERIES = '|'.join(e.name for e in SpecialSeries)
PATTERN_NON_BUSINESS_SPECIAL_SERIES = '|'.join(e.name for e in NonBusinessSpecialSeries)
PATTERN_SPECIAL_ECONOMIC_ZONE_SERIES = '|'.join(e.name for e in SpecialEconomicZoneSeries)
# Letters used for automobile series registered since 2010
PATTERN_PERMITTED_LETTERS = '[A-HK-NPS-VXYZ]'
# Letters which were used in automobile series before 2010, but no longer used since 2010
PATTERN_OBSOLETE_LETTERS = '[IJOQR]'

REGEXES = {
    # If the plate contains obsolete (pre-2010) letters, the order must be 4-digit.
    # otherwise, the order can be 4 or 5 digits.
    VehicleType.DOMESTIC_AUTOMOBILE: re.compile(
        r'(?P<locality>\d{2})'
        rf'(?P<series>{PATTERN_PERMITTED_LETTERS}|(?P<obsolete_letter>{PATTERN_OBSOLETE_LETTERS}))'
        r'(?P<order>(?(obsolete_letter)\d{4}|\d{4,5}))'
    ),
    # FIXME: This one is quite problematic
    # Example: 80NG-636-70, 80QT-546-42, 80NN-381-35, 80-011-NG-01, 80-631-CV-01
    VehicleType.DIPLOMATIC: re.compile(
        r'(?P<locality>\d{2})'
        r'(?P<country>\d{3})?'
        r'(?P<series>(NG|QT|NN|CV))'
        r'(?P<order>\d{2,5})',
    ),
    VehicleType.SPECIAL_BUSINESS: re.compile(
        r'(?P<locality>\d{2})'
        f'(?P<series>{PATTERN_SPECIAL_SERIES})'
        r'(?P<order>\d{4,5})'
    ),
    VehicleType.SPECIAL_ECONOMIC_ZONE: re.compile(
        r'(?P<locality>\d{2})'
        f'(?P<series>{PATTERN_SPECIAL_ECONOMIC_ZONE_SERIES})'
        r'(?P<order>\d{4,5})'
    ),
    VehicleType.NON_BUSINESS_SPECIAL: re.compile(
        r'(?P<locality>\d{2})'
        f'(?P<series>(?:{PATTERN_NON_BUSINESS_SPECIAL_SERIES})\\d?)'
        r'(?P<order>\d{4,5})'
    ),
    # Be careful that this plate may be mistaken with the special ones above, with two-letter series
    VehicleType.DOMESTIC_MOTORCYCLE_UNDER_50CC: re.compile(
        r'(?P<locality>\d{2})'
        r'(?P<series>[A-HK-NPS-VXYZ][A-FHK-NPR-VXYZ])'
        r'(?P<order>\d{4,5})',
    ),
    VehicleType.DOMESTIC_MOTORCYCLE_50_TO_175CC: re.compile(
        r'(?P<locality>\d{2})'
        r'(?P<series>[B-Z][1-9])'
        r'(?P<order>\d{4,5})'
    ),
    VehicleType.DOMESTIC_MOTORCYCLE_OVER_175CC: re.compile(
        r'(?P<locality>\d{2})'
        r'(?P<series>A[1-9])'
        r'(?P<order>\d{4,5})'
    ),
    # Example: TC3386
    VehicleType.MILITARY: re.compile(r'(?P<series>[A-DHKPQTV][A-X]B?)(?P<order>\d{4})'),
    # The temporary plate doesn't have series
    VehicleType.TEMPORARY: re.compile(r'(?P<series>T)(?P<locality>\d{2})(?P<order>\d{5})'),
}


@dataclass
class VietnamVehiclePlate:
    """Class to represent a Vietnamese vehicle number plate.

    Library user must not create instance directly from this class constructer.
    Please call :meth:`VietnamVehiclePlate.from_string` instead.

    :param vehicle_type: Type of vehicle (of :class:`VehicleType` type), deduced from the plate number.
    :param series: Series string of the plate number.
    :param order: Registration order number.
    :param locality: Locality where this vehicle was registered.
    :param dip_country: Foreign country where the vehicle owner came from (in case of diplomat, foreigner use).
    """

    vehicle_type: VehicleType
    series: str
    order: str
    locality: Optional[str] = None
    dip_country: Optional[str] = None

    @memoized_property
    def compact(self):
        """
        Compact string of plate number, where all characters other than letters and numbers are stripped.

        If we are about to serialize and save this object, the compact form should be used.
        """
        locality = self.locality or ''
        dip_country = self.dip_country or ''
        return f'{locality}{dip_country}{self.series}{self.order}'

    def __len__(self):
        """Return the length of this object, if it is about to be saved some where as string."""
        return len(self.compact)

    def __str__(self):
        """Return string representation of this object."""
        vehicle_type = self.vehicle_type
        mototcycle_types = (VehicleType.DOMESTIC_MOTORCYCLE_UNDER_50CC, VehicleType.DOMESTIC_MOTORCYCLE_OVER_175CC,
                            VehicleType.DOMESTIC_MOTORCYCLE_50_TO_175CC)
        if len(self.order) <= 4:
            order = self.order
        else:
            # For number plate since 2010, the order will be separated with dot,
            # to be easier to read.
            order = '.'.join(split_to_triples(self.order))
        if vehicle_type in mototcycle_types:
            return f'{self.locality}-{self.series} {order}'
        return f'{self.locality}{self.series}-{order}'

    @classmethod
    def from_string(cls, number_sequence: str) -> 'VietnamVehiclePlate':
        """Parse the number string of Vietnamese vehicle registration plate.

        :param number_sequence: Number string as printed on the plate.
        :return: :class:`VietnamVehiclePlate` object.
        :raises ValueError: If the number string could not be parsed.
        :raises TypeError: If the passed value is not a string.
        """
        if not isinstance(number_sequence, str):
            raise TypeError(f'Need a string, not {type(number_sequence)} type!')
        compact = REGEX_CLEAN_PLATE_NUMBER.sub('', number_sequence.upper())
        if not compact:
            raise ValueError('Empty string!')
        for vtype, regex in REGEXES.items():
            m = regex.fullmatch(compact)
            if not m:
                continue
            data = {
                'vehicle_type': vtype,
                'order': m.group('order')
            }
            try:
                data['locality'] = m.group('locality')
            except IndexError:
                pass
            try:
                data['series'] = m.group('series')
            except IndexError:
                pass
            try:
                data['dip_country'] = m.group('country')
            except IndexError:
                pass
            return VietnamVehiclePlate(**data)
        else:
            # Not found match
            raise ValueError('Unrecognized plate number')
