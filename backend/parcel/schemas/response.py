from pydantic import BaseModel

from parcel.model import ParcelStatusEnum, ParcelDeliveryPartnerEnum


class ParcelInDB(BaseModel):
    id: int
    awn_number: str
    delivery_partner: ParcelDeliveryPartnerEnum
    status: ParcelStatusEnum
    created_at: int
    updated_at: int
    date: int