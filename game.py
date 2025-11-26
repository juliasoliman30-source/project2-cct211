class Game:
    def __init__(self, id, title, platform, status, rating=0, hours_played=0, imagePath=""):
        self.id = id
        self.title = title
        self.platform = platform
        self.status = status  # "completed", "ongoing", "backlog", "wishlist"
        self.rating = rating
        self.hours_played = hours_played
        self.imagePath = imagePath