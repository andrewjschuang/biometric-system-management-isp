from database.MongoConnector import MongoConnector
import config


class ConfigCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        super()._set_collection('config')
        self._init_config()

    def _init_config(self):
        if not self._get_config("video_source"):
            self._insert({"video_source": config.video_source})
        if not self._get_config("tolerance"):
            self._insert({"tolerance": config.tolerance})
        if not self._get_config("active_rate"):
            self._insert({"active_rate": config.active_rate})
        if not self._get_config("delay"):
            self._insert({"delay": config.delay})
        if not self._get_config("display_image"):
            self._insert({"display_image": config.display_image})

    def _get_config(self, config):
        return self.collection.find_one(
            {config: {"$exists": True}},
        )[config]

    def _set_config(self, config, value):
        return self.collection.update_one(
            {config: {"$exists": True}},
            {"$set": {config: value}},
        )

    def get_video_source(self):
        return self._get_config("video_source")

    def set_video_source(self, value):
        return self._set_config("video_source", value)

    def get_tolerance(self):
        return self._get_config("tolerance")

    def set_tolerance(self, value):
        return self._set_config("tolerance", value)

    def get_active_rate(self):
        return self._get_config("active_rate")

    def set_active_rate(self, value):
        return self._set_config("active_rate", value)

    def get_delay(self):
        return self._get_config("delay")

    def set_delay(self, value):
        return self._set_config("delay", value)

    def get_display_image(self):
        return self._get_config("display_image")

    def set_display_image(self, value):
        return self._set_config("display_image", value)
