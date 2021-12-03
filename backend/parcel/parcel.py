from common.utils import get_current_timestamp
from parcel.repos import parcel_repo


class Parcel:
    def __init__(self, user, tracking_status, tracking_ts, awn):
        self.tracking_status = tracking_status
        self.tracking_ts = tracking_ts
        self.awn = awn
        self.user = user
        self.created_at = get_current_timestamp()
        self.updated_at = get_current_timestamp()

    @property
    def tracking_status(self):
        return self._tracking_status

    @tracking_status.setter
    def tracking_status(self, tracking_status):
        self._tracking_status = tracking_status

    @property
    def awn(self):
        return self._awn

    @awn.setter
    def awn(self, awn):
        self._awn = awn

    @property
    def tracking_ts(self):
        return self._tracking_ts

    @tracking_ts.setter
    def tracking_ts(self, tracking_ts):
        self._tracking_ts = tracking_ts

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user


    async def get_latest_parcel(self):
        return await parcel_repo.get_latest_parcel(user_id=self.user)
