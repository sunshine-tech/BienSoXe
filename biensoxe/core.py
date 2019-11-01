# Ref:
# https://thuvienphapluat.vn/van-ban/Giao-thong-Van-tai/Thong-tu-15-2014-TT-BCA-quy-dinh-ve-dang-ky-xe-Bo-truong-Bo-Cong-an-229224.aspx
# https://danluat.thuvienphapluat.vn/ban-da-biet-gi-ve-bien-so-xe-132978.aspx
# https://tuoitre.vn/2800-xe-bon-banh-khong-biet-xep-vao-loai-xe-gi-1078666.htm

import re
import enum

from pydantic import constr
from pydantic.dataclasses import dataclass


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
    # https://banotore.com/xe-xe-tai-tren-10-tan-ba-ria-vung-tau/ban-tra-gop-lai-suat-thap-so-mi-ro-mooc-san-doosung-40feet3truc-aid563816
    R = 'R'   # 51R-14139


class SpecialEconomicZoneSeries(enum.Enum):
    ''' This plate has yellow background '''
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
    TRACTOR_AND_ELECTRIC = enum.auto()
    FOREIGN_AUTOMOBILE = enum.auto()
    FOREIGN_MOTORCYCLE = enum.auto()
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
REGEXES = {
    VehicleType.DOMESTIC_AUTOMOBILE: re.compile(r'''(?P<locality>\d{2})
                                                (?P<series>[A-HK-NPS-VXYZ])
                                                \d{4,5}''',
                                                re.VERBOSE),
    # FIXME: This one is quite problematic
    # Example: 80NG-636-70, 80QT-546-42, 80NN-381-35, 80-011-NG-01, 80-631-CV-01
    VehicleType.DIPLOMATIC: re.compile(r'''(?P<locality>\d{2})
                                       (?P<country>\d{3})?
                                       (?P<series>(NG|QT|NN|CV))
                                       \d{2,5}''',
                                       re.VERBOSE),
    VehicleType.SPECIAL_BUSINESS: re.compile(r'(?P<locality>\d{2})'
                                             + f'(?P<series>{PATTERN_SPECIAL_SERIES})'
                                             + r'\d{4,5}'),
    VehicleType.SPECIAL_ECONOMIC_ZONE: re.compile(r'(?P<locality>\d{2})'
                                                  + f'(?P<series> {PATTERN_SPECIAL_ECONOMIC_ZONE_SERIES})'
                                                  + r'\d{4,5}'),
    VehicleType.NON_BUSINESS_SPECIAL: re.compile(r'(?P<locality>\d{2})'
                                                 + f'(?P<series> {PATTERN_NON_BUSINESS_SPECIAL_SERIES})'
                                                 + r'\d{4,5}'),
    # Be careful that this plate may be mistaken with the special ones above, with two-letter series
    VehicleType.DOMESTIC_MOTORCYCLE_UNDER_50CC: re.compile(r'''(?P<locality>\d{2})
                                                           (?P<series>[A-HK-NPS-VXYZ][A-FHK-NPR-VXYZ])
                                                           \d{4,5}''',
                                                           re.VERBOSE),
    VehicleType.DOMESTIC_MOTORCYCLE_50_TO_175CC: re.compile(r'(?P<locality>\d{2})'
                                                            r'(?P<series>[B-Z][1-4])\d{4,5}'),
    VehicleType.DOMESTIC_MOTORCYCLE_OVER_175CC: re.compile(r'(?P<locality>\d{2})'
                                                           r'(?P<series>A[1-9])\d{4,5}'),
    # Example: TC3386
    VehicleType.MILITARY: re.compile(r'[A-DHKPQTV][A-X]B?\d{4}'),
    # The temporary plate doesn't have series
    VehicleType.TEMPORARY: re.compile(r'T(?P<locality>\d{2})\d{5}'),
}


@dataclass
class VietnamVehiclePlate:
    compact: constr(regex=f'[a-zA-Z0-9]+')
    vehicle_type: VehicleType
    locality: str
    series: str
    dip_country: str
