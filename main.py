from settings import Settings
from prepare_photos import scan_photos
from reorder_photos import reorder_photos


settings = Settings("settings.json")

scan_photos(settings, True)
reorder_photos(settings, True)
