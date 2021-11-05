from typing import Optional

from pydantic import BaseModel

from common.int_choice import IntChoice

class PTBaseModel(BaseModel):
    created_at: int
    updated_at: Optional[int]

class ParcelDeliveryPartnerEnum(IntChoice):
    AMAZON= 1
    FLIPKART= 2
    BLUEDART= 3
    ECOM_EXPRESS= 4
    DELHIVERY= 5
    FEDEX= 6

class ParcelStatusEnum(IntChoice):
    DELIVERED= 1
    IN_TRANSIT= 2


class Parcel(PTBaseModel):
    id: int
    awn_number: str
    delivery_partner: ParcelDeliveryPartnerEnum
    status: ParcelStatusEnum
    date: int