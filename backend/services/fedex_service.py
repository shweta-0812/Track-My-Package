import datetime
from typing import Dict, Any

import aiohttp

# awn num: 284932411496
from parcel.models import ParcelStatusEnum


async def get_fedex_parcel_details(awn_number: str) ->Dict[str, Any]:
    fedex_delivery_details = await get_fedex_api_response(
        awn_number=awn_number)
    delivery_details = dict()
    if fedex_delivery_details["status"] == "Delivered":
        delivery_details["status"] = ParcelStatusEnum.DELIVERED.value
        delivery_date_str = fedex_delivery_details["date"]
        delivery_dt_obj = datetime.datetime.strptime(delivery_date_str,
                                                     "%d/%m/%Y")
        delivery_ts = datetime.datetime.timestamp(delivery_dt_obj)
        delivery_details["date"] = int(delivery_ts)



async def get_fedex_api_response(awn_number: str):
    parcel_tracking_details_dict = dict()
    string_data = f"action=trackpackages&data=%7B%22TrackPackagesRequest%22:%7B%22appDeviceType%22:%22DESKTOP%22,%22appType%22:%22WTRK%22,%22processingParameters%22:%7B%7D,%22uniqueKey%22:%22%22,%22supportCurrentLocation%22:true,%22supportHTML%22:true,%22trackingInfoList%22:%5B%7B%22trackNumberInfo%22:%7B%22trackingNumber%22:%22{awn_number}%22,%22trackingQualifier%22:%222459503000~284932411496~FX%22,%22trackingCarrier%22:null%7D%7D%5D%7D%7D&format=json&locale=en_IN&version=1"
    bytes_data = bytes(string_data, "utf-8")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://www.fedex.com/trackingCal/track",
            headers={
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
            data=bytes_data,
        ) as response:
            api_resp = await response.json(content_type="text/html")
            # parcel_tracking_details_dict[''] = api_resp["TrackPackagesResponse"]["packageList"][0]["displayTrackingNbr"]
            parcel_tracking_details_dict["date"] = api_resp["TrackPackagesResponse"][
                "packageList"
            ][0]["displayActDeliveryDt"]
            parcel_tracking_details_dict["status"] = api_resp["TrackPackagesResponse"][
                "packageList"
            ][0]["keyStatus"]
    return parcel_tracking_details_dict