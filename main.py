from settings import Settings
from prepare_photos import scan_photos


settings = Settings("settings.json")

scan_photos(settings, True)
