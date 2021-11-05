from pydantic import BaseModel

from parcel.models import ParcelStatusEnum, ParcelDeliveryPartnerEnum


class Parcel(BaseModel):
    id: int
    awn_number: str
    delivery_partner: ParcelDeliveryPartnerEnum
    status: ParcelStatusEnum
    created_at: int
    updated_at: int
    date: int