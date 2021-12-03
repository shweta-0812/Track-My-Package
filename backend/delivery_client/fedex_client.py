import aiohttp

from delivery_client.base_delivery_client import BaseTrackingService
from parcel.model import ParcelDeliveryPartnerEnum


class Fedex(BaseTrackingService):
    def __init__(self, awn):
        super().__init__(awn=awn, delivery_partner=ParcelDeliveryPartnerEnum.FEDEX.value)

    async def make_request_to_delivery_partner_service(self):
        string_data = f"action=trackpackages&data=%7B%22TrackPackagesRequest%22:%7B%22appDeviceType%22:%22DESKTOP%22,%22appType%22:%22WTRK%22,%22processingParameters%22:%7B%7D,%22uniqueKey%22:%22%22,%22supportCurrentLocation%22:true,%22supportHTML%22:true,%22trackingInfoList%22:%5B%7B%22trackNumberInfo%22:%7B%22trackingNumber%22:%22{self.awn}%22,%22trackingQualifier%22:%222459503000~284932411496~FX%22,%22trackingCarrier%22:null%7D%7D%5D%7D%7D&format=json&locale=en_IN&version=1"
        bytes_data = bytes(string_data, "utf-8")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "https://www.fedex.com/trackingCal/track",
                    headers={
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                    },
                    data=bytes_data,
            ) as response:
                self.delivery_partner_api_resp = await response.json(content_type="text/html")


    async def parse_delivery_partner_service_response(self):
        self.tracking_date = self.delivery_partner_api_resp["TrackPackagesResponse"]["packageList"][0]["displayActDeliveryDt"]
        self.status = self.delivery_partner_api_resp["TrackPackagesResponse"]["packageList"][0]["keyStatus"]

    async def fetch_tracking_details(self):
        await self.make_request_to_delivery_partner_service()
        await self.parse_delivery_partner_service_response()
