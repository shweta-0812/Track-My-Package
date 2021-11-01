from typing import Any

import aiohttp
from bs4 import BeautifulSoup

from common.base_repo import get_current_timestamp
from parcel.interactors.repos import parcel_repo
from parcel.models import ParcelDeliveryPartnerEnum
from parcel.schema import CreateParcel

does_index_exists = parcel_repo.does_index_exists
create_index = parcel_repo.create_index
cat_indices = parcel_repo.cat_indices

get_parcel = parcel_repo.get_parcel
get_latest_parcel = parcel_repo.get_latest_parcel


async def get_parcel_tracking_details_from_delivery_partner(
    awn_number: str, delivery_partner: int
) -> Any:
    delivery_details = dict()
    if delivery_partner == ParcelDeliveryPartnerEnum.BLUEDART.value:
        bluedart_delivery_details = await get_bluedart_webpage_response(
            awn_number=awn_number
        )
        delivery_details["status"] = bluedart_delivery_details["overview"]["Status"]
        delivery_details["date"] = bluedart_delivery_details["overview"][
            "Date of Delivery"
        ]
    return delivery_details


async def create_parcel(create_parcel: CreateParcel):
    new_parcel_data = dict()
    # latest_parcel = await get_latest_parcel()
    # last_id = 0
    # if latest_parcel["hits"]["total"]["value"] > 0:
    #     last_id = latest_parcel["hits"]["hits"][0]["_id"]
    #
    # # auto generate new id
    # new_parcel_data["id"] = last_id + 1

    # calculate
    parcel_tracking_details = await get_parcel_tracking_details_from_delivery_partner(
        awn_number=create_parcel.awn_number,
        delivery_partner=create_parcel.delivery_partner,
    )
    new_parcel_data["status"] = parcel_tracking_details["status"]
    new_parcel_data["date"] = parcel_tracking_details["date"]
    new_parcel_data["created_at"] = get_current_timestamp()
    new_parcel_data["awn_number"] = create_parcel.awn_number
    new_parcel_data["delivery_partner"] = create_parcel.delivery_partner
    return None
    # return await parcel_repo.create_parcel(parcel=Parcel(**new_parcel_data))


async def get_parcels_list():
    return await parcel_repo.get_parcels()


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


#
#
# @app.get("/ecomexpress/web-response/")
# async def get_webpage_response():
#     req_client = HTTPClient(host="ecomexpress.in/", scheme="https")
#     page = await req_client.get(path="tracking/", params=[("awb_field", 2792380736)])
#     page_html = page.text
#     tree = html.fromstring(page.content)
#
#     awn_number = tree.xpath('//span[@class="awb-number-value"]/text()')
#     order_number = tree.xpath('//span[@class="order-number-value"]/text()')
#     current_status = tree.xpath('//span[@class="current-status-value"]/text()')
#     return current_status
#
#
# @app.get("/delivery/api-response/")
# async def get_api_response():
#     req_client = HTTPClient(host="dlv-web-api.delhivery.com/v3/", scheme="https")
#     resp = await req_client.get(path="track", params=[("wbn", 425110283544)])
#     return resp.json()
#

#
# @app.get("/delivery/api-response/")
# async def get_api_response():
#     req_client =  HTTPClient(host='dlv-web-api.delhivery.com/v3/',scheme='https')
#     resp = await req_client.get(path='track', params=[('wbn',425110283544)])
#     return resp.json()
