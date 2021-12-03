from pydantic import BaseModel

from parcel.model import ParcelDeliveryPartnerEnum


class CreateParcel(BaseModel):
    awn: str
    delivery_partner: ParcelDeliveryPartnerEnum
