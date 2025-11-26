import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
from data import *
from fonts import *
from game import *

class GameTracker:
    def __init__(self):
        self.games = []
        self.raw_csv_data = load_data()
        self.create_games()

    def create_games(self):
        """
        Use the data from the csv file to create game entries.
        """
        games_list = []
        for game_data in self.raw_csv_data:
            status = self.normalize_status(game_data.get("Status", ""))

            game = Game(
                id=game_data.get("ID", ""),
                title=game_data.get("Title", ""),
                platform=game_data.get("Platform", ""),
                status=status,
                rating=int(game_data.get("Rating", 0)),
                hours_played=int(game_data.get("Hours", 0)),
                imagePath="pictures/" + game_data.get("ImagePath", "")
            )
            games_list.append(game)
        self.games = games_list

    def normalize_status(self, status):
        """Convert CSV status values to match the code's expected values"""
        status_mapping = {
            "Ongoing": "ongoing",
            "Completed": "completed",
            "Wishlisted": "wishlist",
            "Backlog": "backlog"
        }
        return status_mapping.get(status, status.lower())

    def get_games_by_status(self, status):
        """Get games filtered by status"""
        if status == "all":
            return self.games
        return [game for game in self.games if game.status == status]

    def get_total_games(self):
        """Get total number of games registered"""
        return len(self.games)

    def get_completed_percentage(self):
        """Get percentage of completed games"""
        if not self.games:
            return 0
        completed_count = len([game for game in self.games if game.status == "completed"])
        return round((completed_count / len(self.games)) * 100)

    def get_total_hours_played(self):
        """Get total hours played across all games"""
        return sum(game.hours_played for game in self.games if game.hours_played > 0)

    def get_games_by_status_count(self, status):
        """Get count of games by status"""
        return len([game for game in self.games if game.status == status])

    def add_game(self, title, platform, status, hours, rating, imagePath=""):
        """
        Add the given entry to the current games list and write it to the csv file.
        """
        newId = generate_unique_id(self.raw_csv_data)
        newEntry = {"ID": newId, "Title": title, "Platform": platform, "Status": status, "Hours": hours,
                    "Rating": rating, "ImagePath": imagePath}
        self.raw_csv_data.append(newEntry)
        newGame = Game(
            id=newEntry.get("ID", ""),
            title=newEntry.get("Title", ""),
            platform=newEntry.get("Platform", ""),
            status=newEntry.get("Status", ""),
            rating=int(newEntry.get("Rating", 0)),
            hours_played=int(newEntry.get("Hours", 0)),
            imagePath=newEntry.get("ImagePath", "")
        )
        self.games.append(newGame)
        write_data_to_csv(self.raw_csv_data)

    def edit_game(self, title, platform, status, hours, rating, imagePath=""):
        """
        Update the given entry to the current games list and write it to the CSV file.
        """

        # when editing a specific, find its entry in the CSV file
        for entry in self.raw_csv_data:
            if entry["Title"].lower() == title.lower():
                entry["Platform"] = platform
                entry["Status"] = status
                entry["Hours"] = hours
                entry["Rating"] = rating
                entry["ImagePath"] = imagePath
                break
        else:
            print(f"No game found with title '{title}'")
            return

        # update the corresponding entry and reflect its changes in the CSV file
        for game in self.games:
            if game.title.lower() == title.lower():
                game.platform = platform
                game.status = status
                game.hours_played = int(hours)
                game.rating = int(rating)
                game.imagePath = imagePath
                break
        write_data_to_csv(self.raw_csv_data)