import datetime
from typing import Any, Dict

import aiohttp
from bs4 import BeautifulSoup

# https://www.bluedart.com/web/guest/trackdartresultthirdparty?trackFor=0&trackNo= 62321351396
# awn num 62321351396
from parcel.model import ParcelStatusEnum


async def get_bluedart_parcel_tracking_details(awn_number: str) -> Dict[str, Any]:
    bluedart_delivery_details = await get_bluedart_webpage_response(
        awn_number=awn_number
    )
    delivery_details = dict()
    if bluedart_delivery_details["overview"]["Status"] == "Shipment Delivered":
        delivery_details["status"] = ParcelStatusEnum.DELIVERED.value
        delivery_date_str = bluedart_delivery_details["overview"][
            "Date of Delivery"
        ]
        delivery_dt_obj = datetime.datetime.strptime(delivery_date_str,
                                                     "%d %b %Y")
        delivery_ts = datetime.datetime.timestamp(delivery_dt_obj)
        delivery_details["date"] = int(delivery_ts)


async def get_bluedart_webpage_response(awn_number: str) -> Any:
    parcel_tracking_details_dict = dict()
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.bluedart.com/web/guest/trackdartresult",
            params=[("trackFor", 0), ("trackNo", awn_number)],
        ) as response:
            page_text = await response.text()
            soup = BeautifulSoup(page_text, "html.parser")
            # print(soup.title)

            for liTag in soup.select(".trackDart-box .panel-bd-List > ul > li"):
                labelTag = liTag.select_one("label")
                pTag = liTag.select_one("p")
                parcel_tracking_details_dict[str(labelTag.get_text(strip=True))] = str(
                    pTag.get_text(strip=True)
                )

            parcel_tracking_details_dict["overview"] = {}
            for tableTag in soup.select(
                f".trackDart-box #SHIP{awn_number} .table tbody tr"
            ):
                thTag = tableTag.select_one("th")
                tdTag = tableTag.select_one("td")
                parcel_tracking_details_dict["overview"][
                    str(thTag.get_text(strip=True))
                ] = str(tdTag.get_text(strip=True))

            parcel_tracking_detailed_overview_headers = []
            for tableTag in soup.select(
                f".trackDart-box #SCAN{awn_number} .table thead tr th"
            ):
                if str(tableTag.get_text(strip=True)) != "Status and Scans":
                    parcel_tracking_detailed_overview_headers.append(
                        (tableTag.get_text(strip=True))
                    )

            parcel_tracking_details_dict["detailed_overview"] = []
            for tableTag in soup.select(
                f".trackDart-box #SCAN{awn_number} .table tbody tr"
            ):
                tdTags = tableTag.select("td")

                if len(tdTags) > 1:
                    for i in range(
                        0, len(parcel_tracking_detailed_overview_headers) - 1
                    ):
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