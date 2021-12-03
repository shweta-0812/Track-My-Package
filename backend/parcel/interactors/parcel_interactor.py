import json
from typing import Any

from delivery_client.bluedart_client import Bluedart
from delivery_client.ecom_express_client import EcomExpress
from delivery_client.fedex_client import Fedex
from parcel.model import ParcelDeliveryPartnerEnum
from parcel.parcel import Parcel
from parcel.repos import parcel_repo
from parcel.schemas.request import CreateParcel

does_index_exists = parcel_repo.does_index_exists
create_index = parcel_repo.create_index
delete_index = parcel_repo.delete_index
cat_indices = parcel_repo.cat_indices

get_parcel = parcel_repo.get_parcel
get_latest_parcel = parcel_repo.get_latest_parcel


async def get_parcel_tracking_detail_for_delivery_partner(
    awn: str, delivery_partner: int
) -> Any:
    parcel_tracker_obj = None
    if delivery_partner == ParcelDeliveryPartnerEnum.BLUEDART.value:
        parcel_tracker_obj = Bluedart(awn=awn)
    if delivery_partner == ParcelDeliveryPartnerEnum.ECOM_EXPRESS.value:
        parcel_tracker_obj = EcomExpress(awn=awn)
    if delivery_partner == ParcelDeliveryPartnerEnum.FEDEX.value:
        parcel_tracker_obj = Fedex(awn=awn)
    if parcel_tracker_obj is not None:
        await parcel_tracker_obj.fetch_tracking_details()
    return parcel_tracker_obj


async def create_parcel(create_parcel: CreateParcel, user):
    parcel_tracking_details = await get_parcel_tracking_detail_for_delivery_partner(
        awn=create_parcel.awn,
        delivery_partner=create_parcel.delivery_partner,
    )
    user_parcel = Parcel(awn=parcel_tracking_details._awn, tracking_status=parcel_tracking_details._tracking_status, tracking_ts=parcel_tracking_details._tracking_ts,  user=user)
    new_parcel_data = dict()

    latest_parcel = await user_parcel.get_latest_parcel()
    last_id = 0
    if latest_parcel["hits"]["total"]["value"] > 0:
        last_id = latest_parcel["hits"]["hits"][0]["_id"]

    # auto generate new id
    new_parcel_data["id"] = int(last_id) + 1
    return None
    # return await parcel_repo.create_parcel(parcel=ParcelModelClass(**new_parcel_data))


async def get_parcels_list():
    return await parcel_repo.get_parcels()
