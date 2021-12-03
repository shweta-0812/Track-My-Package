from abc import ABC, abstractmethod


class AWNEmptyError(Exception):
    def __init__(self, awn: str):
        self.awn = awn
        self.message = "AWN is empty"

    def __str__(self):
        pass


class BaseTrackingService(ABC):
    def __init__(self, awn: str, delivery_partner:str):
        self.awn = awn
        self.tracking_status = None
        self.tracking_ts = None
        self.delivery_partner = delivery_partner

    @property
    def awn(self):
        return self._awn

    @awn.setter
    def awn(self, awn: str):
        if awn:
            self._awn = awn
        else:
            raise AWNEmptyError

    @property
    def tracking_status(self):
        return self._tracking_status

    @tracking_status.setter
    def tracking_status(self, status):
        self._tracking_status = status

    @property
    def tracking_ts(self):
        return self._tracking_ts

    @tracking_ts.setter
    def tracking_ts(self, tracking_ts):
        self._tracking_ts = tracking_ts

    @property
    def delivery_partner(self):
        return self._delivery_partner

    @delivery_partner.setter
    def delivery_partner(self, delivery_partner):
        self._delivery_partner = delivery_partner

    @abstractmethod
    async def make_request_to_delivery_partner_service(self):
        pass

    @abstractmethod
    async def parse_delivery_partner_service_response(self, delivery_partner_response):
        pass

    @abstractmethod
    async def fetch_tracking_details(self):
        pass
