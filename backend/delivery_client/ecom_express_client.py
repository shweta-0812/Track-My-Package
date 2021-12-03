import datetime

import aiohttp
from bs4 import BeautifulSoup

from delivery_client.base_delivery_client import BaseTrackingService
from parcel.model import ParcelStatusEnum, ParcelDeliveryPartnerEnum


class EcomExpress(BaseTrackingService):
    def __int__(self, awn):
        super().__init__(awn=awn, delivery_partner=ParcelDeliveryPartnerEnum.ECOM_EXPRESS.value)

    async def make_request_to_delivery_partner_service(self):
        parcel_tracking_details_dict = dict()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://www.ecomexpress.in/tracking/",
                    params=[("awb_field", self.awn)],
            ) as response:
                self.delivery_partner_response_text = await response.text()

    async def parse_delivery_partner_service_response(self):
        soup = BeautifulSoup(self.delivery_partner_response_text, "html.parser")
        self.parcel_tracking_details_dict = {}
        for pTag in soup.select(
                "body .tracking-order-top-sec .track-order-top-sec-col p"
        ):
            spanTags = pTag.select("span")
            label = (spanTags[0].get_text()).replace(":", "")
            value = spanTags[1].get_text()
            self.parcel_tracking_details_dict[label] = value

        self.parcel_tracking_details_dict["overview"] = {}
        self.parcel_tracking_details_dict["overview"]["track_progress"] = []
        for pTag in soup.select(
                "body .track-order-progress .track-order-progress-col p"
        ):
            self.parcel_tracking_details_dict["overview"]["track_progress"].append(
                pTag.get_text()
            )

        thTags = soup.select("body .table-striped thead tr th")
        self.parcel_tracking_details_dict["Date"] = (thTags[0].get_text()).replace(
            ",", ""
        )

    async def get_tracking_details(self):
        await self.make_request_to_delivery_partner_service()
        await self.parse_delivery_partner_service_response()
        delivery_details = dict()
        if self.parcel_tracking_details_dict["Current Status"] == "Delivered":
            delivery_details["status"] = ParcelStatusEnum.DELIVERED.value
            delivery_date_str = self.parcel_tracking_details_dict["Date"]
            delivery_dt_obj = datetime.datetime.strptime(delivery_date_str,
                                                         "%d %b %Y")
            delivery_ts = datetime.datetime.timestamp(delivery_dt_obj)
            delivery_details["date"] = int(delivery_ts)
        del self.parcel_tracking_details_dict
