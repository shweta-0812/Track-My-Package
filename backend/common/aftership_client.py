import aftership
from asgiref.sync import sync_to_async

aftership.api_key='666b2900-4d47-46c5-ae54-9bd4b56b7097'

class  AftershipClient:
    @sync_to_async
    def get_couriers_list(self):
        couriers = aftership.courier.list_couriers()
        return couriers

    @sync_to_async
    def create_tracking(self):
        tracking = aftership.tracking.create_tracking(tracking_id='your_tracking_id')
        return tracking

    @sync_to_async
    def update_tracking(self):
        tracking = aftership.tracking.update_tracking(tracking_id='your_tracking_id')
        return tracking

    @sync_to_async
    def get_tracking_updates(self):
        tracking = aftership.tracking.get_tracking(tracking_id='your_tracking_id')
        return tracking
