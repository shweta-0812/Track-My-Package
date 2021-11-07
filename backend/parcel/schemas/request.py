from pydantic import BaseModel

from parcel.model import ParcelDeliveryPartnerEnum


class CreateParcel(BaseModel):
    awn_number: str
    delivery_partner: ParcelDeliveryPartnerEnum
