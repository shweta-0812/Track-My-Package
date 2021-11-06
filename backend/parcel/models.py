from common.base_model import PTBaseModel
from common.int_choice import IntChoice

PARCEL_MODEL="parcel"


class ParcelDeliveryPartnerEnum(IntChoice):
    AMAZON = 1
    FLIPKART = 2
    BLUEDART = 3
    ECOM_EXPRESS = 4
    DELHIVERY = 5
    FEDEX = 6


class ParcelStatusEnum(IntChoice):
    DELIVERED = 1
    IN_TRANSIT = 2


class Parcel(PTBaseModel):
    id: int
    awn_number: str
    delivery_partner: ParcelDeliveryPartnerEnum
    status: ParcelStatusEnum
    date: int