import aiohttp


# awn num: 425110283544
async def get_delhivery_api_response(awn_number: str):
    parcel_tracking_details_dict = dict()
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://dlv-web-api.delhivery.com/v3/track", params=[("wbn", awn_number)],
        ) as response:
            return await response.json()
