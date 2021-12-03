from delivery_client.base_delivery_client import BaseTrackingService


class Delhivery(BaseTrackingService):
    def __init__(self, awn):
        super().__init__(awn=awn)

    def make_request_to_delivery_partner_service(self):
        pass

    def parse_delivery_partner_service_response(self):
        pass

    def get_tracking_details(self):
        pass
