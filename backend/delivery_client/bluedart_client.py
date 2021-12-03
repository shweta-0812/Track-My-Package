import datetime

import aiohttp
from bs4 import BeautifulSoup

from common.int_choice import IntChoice
from common.utils import get_current_timestamp
from delivery_client.base_delivery_client import BaseTrackingService
from parcel.model import ParcelDeliveryPartnerEnum


class BlueDartParcelStatusEnum(IntChoice):
    DELIVERED = 1
    IN_TRANSIT = 2


class Bluedart(BaseTrackingService):
    def __init__(self, awn: str):
        super().__init__(awn=awn, delivery_partner=ParcelDeliveryPartnerEnum.BLUEDART.value)

    async def make_request_to_delivery_partner_service(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.bluedart.com/web/guest/trackdartresult",
                params=[("trackFor", 0), ("trackNo", self.awn)],
            ) as response:
                delivery_partner_response = await response.text()
        return delivery_partner_response

    async def parse_delivery_partner_service_response(self, delivery_partner_response):
        parcel_tracking_details_dict = {}
        soup = BeautifulSoup(delivery_partner_response, "html.parser")
        # print(soup.title)

        for liTag in soup.select(".trackDart-box .panel-bd-List > ul > li"):
            labelTag = liTag.select_one("label")
            pTag = liTag.select_one("p")
            parcel_tracking_details_dict[str(labelTag.get_text(strip=True))] = str(
                pTag.get_text(strip=True)
            )

        parcel_tracking_details_dict["overview"] = {}
        for tableTag in soup.select(f".trackDart-box #SHIP{self.awn} .table tbody tr"):
            thTag = tableTag.select_one("th")
            tdTag = tableTag.select_one("td")
            parcel_tracking_details_dict["overview"][
                str(thTag.get_text(strip=True))
            ] = str(tdTag.get_text(strip=True))

        parcel_tracking_detailed_overview_headers = []
        for tableTag in soup.select(
            f".trackDart-box #SCAN{self.awn} .table thead tr th"
        ):
            if str(tableTag.get_text(strip=True)) != "Status and Scans":
                parcel_tracking_detailed_overview_headers.append(
                    (tableTag.get_text(strip=True))
                )

        parcel_tracking_details_dict["detailed_overview"] = []
        for tableTag in soup.select(f".trackDart-box #SCAN{self.awn} .table tbody tr"):
            tdTags = tableTag.select("td")

            if len(tdTags) > 1:
                for i in range(0, len(parcel_tracking_detailed_overview_headers) - 1):
                    header = parcel_tracking_detailed_overview_headers[i]
                    # print(":::header::::::::::")
                    # print(header)
                    value = str(tdTags[i].get_text(strip=True))
                    # print(":::elem::::")
                    detailed_overview = {}
                    detailed_overview[header] = value
                    parcel_tracking_details_dict["detailed_overview"].append(
                        detailed_overview
                    )
        return parcel_tracking_details_dict

    async def fetch_tracking_details(self):
        delivery_partner_response = await self.make_request_to_delivery_partner_service()
        parcel_tracking_details_dict = None
        if delivery_partner_response:
            parcel_tracking_details_dict = await self.parse_delivery_partner_service_response(delivery_partner_response)

        if parcel_tracking_details_dict["overview"]:
            if parcel_tracking_details_dict["overview"]["Status"] == "Shipment Delivered":
                self.tracking_status = BlueDartParcelStatusEnum.DELIVERED.value
                delivery_date_str = parcel_tracking_details_dict["overview"][
                    "Date of Delivery"
                ]
                delivery_dt_obj = datetime.datetime.strptime(delivery_date_str, "%d %b %Y")
                delivery_ts = datetime.datetime.timestamp(delivery_dt_obj)
                self.tracking_ts = int(delivery_ts)
        if parcel_tracking_details_dict["Status"] == "In Transit Await Delivery Information":
            self.tracking_status = BlueDartParcelStatusEnum.IN_TRANSIT.value
            self.tracking_ts = int(get_current_timestamp())
