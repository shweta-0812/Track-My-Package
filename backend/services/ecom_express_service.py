import datetime
from typing import Dict, Any

import aiohttp
from bs4 import BeautifulSoup

# awn_number:  2792380736
from parcel.model import ParcelStatusEnum


async def get_ecom_express_parcel_tracking_details(awn_number: str) -> Dict[str, Any]:
    ecom_exp_delivery_details = await get_ecomexpress_webpage_response(
        awn_number=awn_number
    )
    delivery_details = dict()
    if ecom_exp_delivery_details["Current Status"] == "Delivered":
        delivery_details["status"] = ParcelStatusEnum.DELIVERED.value
        delivery_date_str = ecom_exp_delivery_details["Date"]
        delivery_dt_obj = datetime.datetime.strptime(delivery_date_str,
                                                     "%d %b %Y")
        delivery_ts = datetime.datetime.timestamp(delivery_dt_obj)
        delivery_details["date"] = int(delivery_ts)


async def get_ecomexpress_webpage_response(awn_number: str):
    parcel_tracking_details_dict = dict()
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.ecomexpress.in/tracking/", params=[("awb_field", awn_number)],
        ) as response:
            page_text = await response.text()
            soup = BeautifulSoup(page_text, "html.parser")

            for pTag in soup.select(
                "body .tracking-order-top-sec .track-order-top-sec-col p"
            ):
                spanTags = pTag.select("span")
                label = (spanTags[0].get_text()).replace(":", "")
                value = spanTags[1].get_text()
                parcel_tracking_details_dict[label] = value

            parcel_tracking_details_dict["overview"] = {}
            parcel_tracking_details_dict["overview"]["track_progress"] = []
            for pTag in soup.select(
                "body .track-order-progress .track-order-progress-col p"
            ):
                parcel_tracking_details_dict["overview"]["track_progress"].append(
                    pTag.get_text()
                )

            thTags = soup.select("body .table-striped thead tr th")
            parcel_tracking_details_dict["Date"] = (thTags[0].get_text()).replace(
                ",", ""
            )
    return parcel_tracking_details_dict