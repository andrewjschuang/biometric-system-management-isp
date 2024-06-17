from database.MongoConnector import MongoConnector
import config


class ConfigCollection(MongoConnector):
    def __init__(self):
        super().__init__()
        super()._set_collection('config')
        self._init_config()

    def _init_config(self):
        if self._get_config("video_source") is None:
            self._set_config("video_source", config.video_source)
        if self._get_config("tolerance") is None:
            self._set_config("tolerance", config.tolerance)
        if self._get_config("active_rate") is None:
            self._set_config("active_rate", config.active_rate)
        if self._get_config("delay") is None:
            self._set_config("delay", config.delay)
        if self._get_config("display_image") is None:
            self._set_config("display_image", config.display_image)
        if self._get_config("enable_match_confirmation") is None:
            self._set_config("enable_match_confirmation",
                             config.enable_match_confirmation)
        if self._get_config("show_only_sundays") is None:
            self._set_config("show_only_sundays", config.show_only_sundays)

    def _get_config(self, config):
        result = self.collection.find_one({config: {"$exists": True}})
        if result:
            return result[config]

    def _set_config(self, config, value):
        return self.collection.update_one(
            {config: {"$exists": True}},
            {"$set": {config: value}},
            upsert=True,
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

    def get_enable_match_confirmation(self):
        return self._get_config("enable_match_confirmation")

    def set_enable_match_confirmation(self, value):
        return self._set_config("enable_match_confirmation", value)

    def get_show_only_sundays(self):
        return self._get_config("show_only_sundays")

    def set_show_only_sundays(self, value):
        return self._set_config("show_only_sundays", value)
