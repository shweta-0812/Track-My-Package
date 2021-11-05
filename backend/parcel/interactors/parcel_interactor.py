from typing import Any

from common.utils import get_current_timestamp
from parcel.models import ParcelDeliveryPartnerEnum, Parcel
from parcel.repos import parcel_repo
from parcel.schemas.request import CreateParcel
from services.bluedart_service import get_bluedart_parcel_tracking_details
from services.ecom_express_service import \
    get_ecom_express_parcel_tracking_details
from services.fedex_service import get_fedex_parcel_details

does_index_exists = parcel_repo.does_index_exists
create_index = parcel_repo.create_index
delete_index = parcel_repo.delete_index
cat_indices = parcel_repo.cat_indices

get_parcel = parcel_repo.get_parcel
get_latest_parcel = parcel_repo.get_latest_parcel


async def get_parcel_tracking_details_from_delivery_partner(
    awn_number: str, delivery_partner: int
) -> Any:
    delivery_details = dict()
    if delivery_partner == ParcelDeliveryPartnerEnum.BLUEDART.value:
        delivery_details = await get_bluedart_parcel_tracking_details(
            awn_number=awn_number
        )
    if delivery_partner == ParcelDeliveryPartnerEnum.ECOM_EXPRESS.value:
        delivery_details = await get_ecom_express_parcel_tracking_details(
            awn_number=awn_number
        )
    if delivery_partner == ParcelDeliveryPartnerEnum.FEDEX.value:
        delivery_details = await get_fedex_parcel_details(awn_number=awn_number)
    return delivery_details


async def create_parcel(create_parcel: CreateParcel):
    new_parcel_data = dict()
    latest_parcel = await get_latest_parcel()
    last_id = 0
    if latest_parcel["hits"]["total"]["value"] > 0:
        last_id = latest_parcel["hits"]["hits"][0]["_id"]

    # auto generate new id
    new_parcel_data["id"] = int(last_id) + 1

    # calculate
    parcel_tracking_details = await get_parcel_tracking_details_from_delivery_partner(
        awn_number=create_parcel.awn_number,
        delivery_partner=create_parcel.delivery_partner,
    )
    new_parcel_data["status"] = parcel_tracking_details["status"]
    new_parcel_data["date"] = parcel_tracking_details["date"]
    new_parcel_data["awn_number"] = create_parcel.awn_number
    new_parcel_data["created_at"] = get_current_timestamp()
    new_parcel_data["updated_at"] = get_current_timestamp()

    new_parcel_data["delivery_partner"] = create_parcel.delivery_partner.value
    return await parcel_repo.create_parcel(parcel=Parcel(**new_parcel_data))


async def get_parcels_list():
    return await parcel_repo.get_parcels()
