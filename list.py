import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
from data import *
from fonts import *
import os
import shutil


class Game:
    def __init__(self, id, title, platform, status, rating=0, hours_played=0, imagePath=""):
        self.id = id
        self.title = title
        self.platform = platform
        self.status = status  # "completed", "ongoing", "backlog", "wishlist"
        self.rating = rating
        self.hours_played = hours_played
        self.imagePath = imagePath


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
        """Convert CSV status values to match your code's expected values"""
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
            imagePath="pictures/" + newEntry.get("ImagePath", "")
        )
        self.games.append(newGame)
        write_data_to_csv(self.raw_csv_data)


class GameEntry(ctk.CTkFrame):
    def __init__(self, home_frame, master, game, tracker, **kwargs):
        super().__init__(master, **kwargs)
        self.game = game
        self.tracker = tracker
        self.configure(fg_color="#E8E8E8", corner_radius=8, height=60)

        self.setup_entry(home_frame)

    def setup_entry(self, home_frame):
        # Configure grid layout
        self.grid_columnconfigure(0, weight=2, minsize=300)  # Title
        self.grid_columnconfigure(1, weight=1, minsize=150)  # Status
        self.grid_columnconfigure(2, weight=1, minsize=150)  # Platform
        self.grid_columnconfigure(3, weight=1, minsize=150)  # Hours Played
        self.grid_columnconfigure(4, weight=0, minsize=100)  # Actions

        # Game Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.assign_image_icon(title_frame, self.game.imagePath)

        # title text
        title_label = ctk.CTkLabel(title_frame, text=self.game.title,font=ENTRY_FONT(),text_color="#2C2C2C")
        title_label.pack(side=ctk.LEFT)

        # Status
        status_color = self.get_status_color(self.game.status)
        status_text = self.game.status.upper()
        if status_text == "WISHLIST":
            status_text = "WISHLISTED"

        status_label = ctk.CTkLabel(self, text=status_text,font=ENTRY_FONT(),text_color="white",fg_color=status_color,corner_radius=12)
        status_label.grid(row=0, column=1, padx=20, pady=15, sticky="w")

        # Platform
        platform_frame = ctk.CTkFrame(self, fg_color="transparent")
        platform_frame.grid(row=0, column=2,padx=(30, 0),pady=15,sticky="nsew")

        platform_label = ctk.CTkLabel(
            platform_frame,
            text=self.game.platform,
            font=ENTRY_FONT(),
            text_color="#2C2C2C"
        )
        platform_label.pack(anchor="center")

        # Hours played
        hours_text = str(self.game.hours_played) if self.game.hours_played > 0 or self.game.status in ["ongoing","completed"] else "--"
        hours_label = ctk.CTkLabel(self, text=hours_text,font=ENTRY_FONT(),text_color="#2C2C2C")
        hours_label.grid(row=0, column=3,padx=(80, 0),pady=15,sticky="w")

        # Action buttons
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=0, column=4, padx=20, pady=15, sticky="e")

        # edit button
        edit_img = Image.open("pictures/edit_icon.png")
        edit_icon = ctk.CTkImage(edit_img, size=(16, 16))
        edit_button = ctk.CTkButton(actions_frame, image=edit_icon, text="", width=16, height=16,
                                    fg_color="transparent", hover=False, command=self.edit_game)
        edit_button.pack(side=ctk.LEFT, padx=5)

        # delete button
        delete_img = Image.open("pictures/delete_icon.png")
        delete_icon = ctk.CTkImage(delete_img, size=(16, 16))
        delete_button = ctk.CTkButton(actions_frame, image=delete_icon, text="", width=16, height=16,
                                      fg_color="transparent", hover=False, command=lambda: self.delete_game(home_frame))
        delete_button.pack(side=ctk.LEFT, padx=5)

    def assign_image_icon(self, parent, icon_path):
        if not icon_path or not os.path.exists(icon_path):
            icon_path = "pictures/defaultIcon.png"

        try:
            img = Image.open(icon_path)
        except Exception:
            img = Image.open("pictures/defaultIcon.png")
        icon_image = ctk.CTkImage(img, size=(30, 30))
        label = ctk.CTkLabel(parent, image=icon_image, text="")
        label.pack(side=ctk.LEFT, padx=(0, 10))
        label.image = icon_image

    def get_status_color(self, status):
        """Return color for status badge"""
        colors = {
            "completed": "#28A745",  # Green
            "ongoing": "#FFC107",  # Yellow
            "backlog": "#6C757D",  # Gray
            "wishlist": "#17A2B8"  # Teal
        }
        return colors.get(status, "#6C757D")

    def edit_game(self):
        """
        Pop up a new window with a form that lets the user update the details of the game.
        """
        print(f"Edit game: {self.game.title}")  # placeholda

    def delete_game(self, home_frame):
        """
        Pop up a Yes/No window to confirm the user's delete action.
        """
        response = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete {self.game.title}?")

        if response == True:
            imagePathToDelete = "" 
            for i, row in enumerate(self.tracker.raw_csv_data):
                if row.get("ID") == self.game.id:
                    imagePathToDelete = row.get("ImagePath", "")
                    self.tracker.raw_csv_data.pop(i)
                    break
            write_data_to_csv(self.tracker.raw_csv_data)
            self.tracker.create_games()
            if imagePathToDelete:
                fullPath = os.path.join("pictures", imagePathToDelete)
                if os.path.exists(fullPath):
                    os.remove(fullPath)
            home_frame.update_stats()


def update_rating(curr_rating, given_rating, stars_list, empty_star_icon, filled_star_icon):
    """
    Update the rating display and the current value to the given_rating
    """
    curr_rating["value"] = given_rating
    for i in range(5):
        if i < given_rating:
            stars_list[i].configure(image=filled_star_icon)
        else:
            stars_list[i].configure(image=empty_star_icon)


def only_nonnegatives(value):
    """
    Returns True to only non-negative numbers
    """
    if value == "":
        return True
    try:
        test_value = float(value)
        if test_value >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


def on_status_change(hours_entry, choice):
    """
    Enables the hours played field when the user selects 'Ongoing' or 'Completed'.
    Disables it otherwise.
    """
    if choice == "Ongoing" or choice == "Completed":
        hours_entry.configure(state="normal")
    else:
        # hours_entry.configure(state="normal")
        hours_entry.delete(0, "end")
        hours_entry.insert(0, "0")
        hours_entry.configure(state="disabled")


def select_image(curr_image_path, image_label):
    """
    Keeps track of the image path the user selected
    """
    filepath = filedialog.askopenfilename(title="Select Game Icon", filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if filepath:
        curr_image_path["path"] = filepath
        filename = os.path.basename(filepath)
        if len(filename) > 20:
            filename = filename[:27] + "..."
        image_label.configure(text=f"Selected: {filename}")


def save_form(window, master, tracker, error_label, title, platform, status, rating, hours, imagePath):
    """
    Validates the input of the form and properly saves the entry and the image to the pictures folder.
    After that, refreshes the UI on the home page to reflect the changes.
    """
    if not title or not platform or not status:
        error_label.configure(text="Please enter all mandatory fields")
        return
    just_filename = ""
    if imagePath:
        just_filename = os.path.basename(imagePath)
        destPath = os.path.join("pictures", just_filename)
        shutil.copy(imagePath, destPath)
    tracker.add_game(title, platform, status, hours, rating, just_filename)
    master.update_stats()
    window.destroy()

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, tracker, **kwargs):
        super().__init__(master, **kwargs)
        self.tracker = tracker
        self.setup_ui()
        self.update_stats()

    def open_new_window(self, title):
        new_window = ctk.CTkToplevel(self)
        new_window.title(title)
        new_window.geometry("1200x1000")
        new_window.configure(fg_color="#334669")

        # status from title
        status_map = {
            "All Video Games": "all",
            "Completed Video Games": "completed",
            "Ongoing Video Games": "ongoing",
            "Backlogged Video Games": "backlog",
            "Wishlisted Video Games": "wishlist"
        }
        status = status_map.get(title, "all")

        # Page title
        title_text = title.replace(" Video Games", "").upper()
        title_label = ctk.CTkLabel(new_window, text=title_text,
                                font=("Arial", 48, "bold"),
                                text_color="white")
        title_label.pack(pady=30)

        # Close button
        close_button = ctk.CTkButton(new_window, text="← Close",
                                    width=200, height=40,
                                    fg_color="#5F7DB0", hover_color="#3D63A1",
                                    corner_radius=10, text_color="white",
                                    font=("Arial", 16, "bold"),
                                    command=new_window.destroy)
        close_button.pack(pady=20)

        # table header
        header_frame = ctk.CTkFrame(new_window, fg_color="#5F7DB0", corner_radius=8, height=50)
        header_frame.pack(fill="x", pady=(0, 10), padx=50)
        header_frame.pack_propagate(False)

        # header for columns grid
        header_frame.grid_columnconfigure(0, weight=2, minsize=300)  # Title
        header_frame.grid_columnconfigure(1, weight=1, minsize=150)  # Status
        header_frame.grid_columnconfigure(2, weight=1, minsize=150)  # Platform
        header_frame.grid_columnconfigure(3, weight=1, minsize=150)  # Hours Played
        header_frame.grid_columnconfigure(4, weight=0, minsize=100)  # actions column?

        # labels for heardeer
        ctk.CTkLabel(header_frame, text="Title",
                    font=("Arial", 18, "bold"),
                    text_color="white").grid(row=0, column=0, padx=20, pady=15, sticky="w")

        ctk.CTkLabel(header_frame, text="Status",
                    font=("Arial", 18, "bold"),
                    text_color="white").grid(row=0, column=1, padx=20, pady=15, sticky="w")

        ctk.CTkLabel(header_frame, text="Platform",
                    font=("Arial", 18, "bold"),
                    text_color="white").grid(row=0, column=2, padx=20, pady=15, sticky="w")

        ctk.CTkLabel(header_frame, text="Hours Played",
                    font=("Arial", 18, "bold"),
                    text_color="white").grid(row=0, column=3, padx=20, pady=15, sticky="w")

        ctk.CTkLabel(header_frame, text="Actions",
                    font=("Arial", 18, "bold"),
                    text_color="white").grid(row=0, column=4, padx=20, pady=15, sticky="e")

        # Create both frame types but don't pack yet
        regular_frame = ctk.CTkFrame(new_window, fg_color="transparent")
        scrollable_frame = ctk.CTkScrollableFrame(new_window, fg_color="transparent", width=900)

        games = self.tracker.get_games_by_status(status)

        if len(games) <= 3:
            # Use regular frame (no scrollbar) for 3 or fewer entries
            regular_frame.pack(fill="x", padx=50, pady=10)  # Only fill horizontally
            content_frame = regular_frame
        else:
            # Use scrollable frame for more than 3 entries -  height based on content
            content_height = min(len(games) * 70, 300)
            scrollable_frame.configure(height=content_height)
            scrollable_frame.pack(fill="x", padx=50, pady=10)
            content_frame = scrollable_frame

        if not games:
            empty_label = ctk.CTkLabel(content_frame,
                                    text=f"No {status} games found.\nClick 'Add Game' to get started!",
                                    font=("Arial", 24),
                                    text_color="white")
            empty_label.pack(pady=50)
        else:
            for game in games:
                entry = GameEntry(self, content_frame, game, self.tracker)
                entry.pack(fill="x", pady=5)

    def open_add_game_window(self):
        """
        Pop up a new window with a form that lets the user add a new game entry.
        """
        new_window = ctk.CTkToplevel(self)
        new_window.title("Add Game Entry Form")
        new_window.geometry("500x700")
        new_window.configure(fg_color="#334669")
        new_window.grab_set()

        ctk.CTkLabel(new_window, text="Add A New Game!", font=("Arial", 32, "bold"), text_color="white").pack(pady=30)

        form_frame = ctk.CTkFrame(new_window, fg_color="#95A6C8", corner_radius=15)
        form_frame.pack(pady=(10, 0), fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Title *", font=("Arial", 16, "bold"), text_color="white").pack(pady=(20, 5), padx=20,anchor="w")
        title_entry = ctk.CTkEntry(form_frame, width=500, height=40, placeholder_text="Enter game title")
        title_entry.pack(padx=20)

        ctk.CTkLabel(form_frame, text="Platform *", font=("Arial", 16, "bold"), text_color="white").pack(pady=(15, 5),padx=20,anchor="w")
        platform_entry = ctk.CTkEntry(form_frame, width=500, height=40, placeholder_text="e.g., PC, Switch, PS5")
        platform_entry.pack(padx=20)

        # status and hours played frame
        status_hours_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        status_hours_frame.pack(padx=20, pady=(15, 5), fill="x")

        status_hours_frame.grid_columnconfigure(0, weight=0)  # status label
        status_hours_frame.grid_columnconfigure(1, weight=1)  # status dropdown
        status_hours_frame.grid_columnconfigure(2, weight=0)  # Hours label
        status_hours_frame.grid_columnconfigure(3, weight=1)  # Hours entry

        ctk.CTkLabel(status_hours_frame, text="Status *", font=("Arial", 16, "bold"), text_color="white").grid(row=0,column=0, sticky="w",padx=(0, 10))

        status_options = ["Ongoing", "Completed", "Backlog", "Wishlisted"]
        status_dropdown = ctk.CTkComboBox(status_hours_frame, width=200, height=40, values=status_options, state="readonly")
        # status_dropdown.set("...")
        status_dropdown.grid(row=0, column=1, sticky="ew", padx=20)

        ctk.CTkLabel(status_hours_frame, text="Hours Played", font=("Arial", 16, "bold"), text_color="white").grid(row=0,column=2,sticky="w",padx=(0,10))

        vcmd = (new_window.register(only_nonnegatives), "%P")
        hours_entry = ctk.CTkEntry(status_hours_frame, width=200, height=40, placeholder_text="0", validate="key",validatecommand=vcmd)
        hours_entry.insert(0, "0")
        hours_entry.configure(state="disabled")
        hours_entry.grid(row=0, column=3, sticky="ew")

        status_dropdown.configure(command=lambda choice: on_status_change(hours_entry, choice))

        # current rating state
        curr_rating = {"value": 0}
        ratings_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        ratings_frame.pack(padx=20, pady=15, fill="x")

        ratings_frame.grid_columnconfigure(0, weight=0)
        ratings_frame.grid_columnconfigure(1, weight=1)
        ratings_frame.grid_columnconfigure(2, weight=0)

        ctk.CTkLabel(ratings_frame, text="Ratings", font=("Arial", 16, "bold"), text_color="white").grid(row=0, column=0,sticky="w")

        empty_star_img = Image.open("pictures/empty_star.png")
        filled_star_img = Image.open("pictures/filled_star.png")
        empty_star_icon = ctk.CTkImage(empty_star_img, size=(30, 30))
        filled_star_icon = ctk.CTkImage(filled_star_img, size=(30, 30))

        stars_button_container = ctk.CTkFrame(ratings_frame, fg_color="transparent")
        stars_button_container.grid(row=0, column=2, sticky="e")

        stars_list = []
        for i in range(5):
            star_label = ctk.CTkLabel(stars_button_container, image=empty_star_icon, text="")
            star_label.pack(side=ctk.LEFT, padx=5)
            star_label.bind("<Button-1>",lambda e, index=i: update_rating(curr_rating, index + 1, stars_list, empty_star_icon,filled_star_icon))
            stars_list.append(star_label)

        # reset button
        reset_button = ctk.CTkButton(stars_button_container, text="Reset", width=60, height=30, fg_color="#3B5469",hover_color="#5A6268", font=("Arial", 12),command=lambda: update_rating(curr_rating, 0, stars_list, empty_star_icon,filled_star_icon))
        reset_button.pack(side=ctk.LEFT, padx=15)

        ctk.CTkLabel(form_frame, text="Game Icon (.png, .jpg, .jpeg files)", font=("Arial", 16, "bold"),text_color="white").pack(pady=(15, 5), padx=20, anchor="w")

        curr_image_path = {"path": ""}

        image_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        image_frame.pack(padx=20, pady=(4, 10))

        selected_image_label = ctk.CTkLabel(image_frame, text="No image selected", text_color="white", font=("Arial", 14))
        selected_image_label.pack(side=ctk.LEFT, padx=(0, 10))

        browse_button = ctk.CTkButton(image_frame, text="Browse", width=100, height=35, fg_color="#3D63A1",
                                    hover_color="#2E4C7C", font=("Arial", 14),
                                    command=lambda: select_image(curr_image_path, selected_image_label))
        browse_button.pack(side=ctk.LEFT)

        error_label = ctk.CTkLabel(form_frame, text="", text_color="#F54646", font=("Arial", 16))
        error_label.pack(pady=(10, 0))

        # save and cancel button frame
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)

        save_button = ctk.CTkButton(buttons_frame, text="Save", width=150, height=40, fg_color="#28A745",hover_color="#218838", font=("Arial", 16, "bold"),command=lambda: save_form(new_window, self, self.tracker, error_label,title_entry.get(), platform_entry.get(),status_dropdown.get(), curr_rating["value"],hours_entry.get(), curr_image_path["path"]))
        save_button.pack(side=ctk.LEFT, padx=10)

        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", width=150, height=40, fg_color="#6C757D",
                                    hover_color="#5A6268", font=("Arial", 16, "bold"), command=new_window.destroy)
        cancel_button.pack(side=ctk.LEFT, padx=10)

    def setup_ui(self):
        self.your_stats = ctk.CTkLabel(self, text="Your Stats",
                                       font=HOME_FRAME_LARGE_FONT(),
                                       fg_color="#334669", text_color="white",
                                       anchor="w")
        self.your_stats.place(relx=0.5, y=30, anchor="n")

        # Stats values
        self.stats_row = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_row.place(relx=0.5, y=125, anchor="n")

        self.registered_games = ctk.CTkLabel(self.stats_row,
                                             text="Games Registered",
                                             font=HOME_FRAME_STATS_FONT(),
                                             fg_color="#334669",
                                             text_color="white")
        self.registered_games.pack(side=ctk.LEFT, padx=70)

        self.per_completed = ctk.CTkLabel(self.stats_row, text="% Completed",
                                          font=HOME_FRAME_STATS_FONT(),
                                          fg_color="#334669",
                                          text_color="white")
        self.per_completed.pack(side=ctk.LEFT, padx=70)

        self.num_hours_played = ctk.CTkLabel(self.stats_row,
                                             text="Hours Played",
                                             font=HOME_FRAME_STATS_FONT(),
                                             fg_color="#334669",
                                             text_color="white")
        self.num_hours_played.pack(side=ctk.LEFT, padx=70)

        # more stats values
        self.stats_values_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_values_frame.place(relx=0.5, y=180, anchor="n")

        self.games_count = ctk.CTkLabel(self.stats_values_frame,
                                        text="0",
                                        font=("Arial", 32, "bold"),
                                        text_color="white")
        self.games_count.pack(side=ctk.LEFT, padx=85)

        self.percent_completed = ctk.CTkLabel(self.stats_values_frame,
                                              text="0%",
                                              font=("Arial", 32, "bold"),
                                              text_color="white")
        self.percent_completed.pack(side=ctk.LEFT, padx=85)

        self.hours_count = ctk.CTkLabel(self.stats_values_frame,
                                        text="0",
                                        font=("Arial", 32, "bold"),
                                        text_color="white")
        self.hours_count.pack(side=ctk.LEFT, padx=85)

        self.your_lists = ctk.CTkLabel(self, text="Your Lists",
                                       font=HOME_FRAME_LARGE_FONT(),
                                       fg_color="#334669", text_color="white",
                                       anchor="w")
        self.your_lists.place(relx=0.5, y=280, anchor="n")  # Moved up since no breakdown

        # Game Button
        self.add_button = ctk.CTkButton(self, text="+ Add Game",
                                        width=200, height=50,
                                        fg_color="#5F7DB0", hover_color="#3D63A1",
                                        corner_radius=15, text_color="white",
                                        font=("Arial", 20, "bold"),
                                        command=lambda: self.open_add_game_window())
        self.add_button.place(relx=0.5, y=380, anchor="n")  # Adjusted position

        # List buttons
        self.button_row = ctk.CTkFrame(self, fg_color="transparent")
        self.button_row.place(relx=0.5, y=450, anchor="n")

        self.all_button = ctk.CTkButton(
            self.button_row, text="All", width=100, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: self.open_new_window("All Video Games")
        )
        self.all_button.pack(side=ctk.LEFT, padx=30)

        self.completed_button = ctk.CTkButton(
            self.button_row, text="Completed", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: self.open_new_window("Completed Video Games")
        )
        self.completed_button.pack(side=ctk.LEFT, padx=30)

        self.ongoing_button = ctk.CTkButton(
            self.button_row, text="Ongoing", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: self.open_new_window("Ongoing Video Games")
        )
        self.ongoing_button.pack(side=ctk.LEFT, padx=30)

        self.backlog_button = ctk.CTkButton(
            self.button_row, text="Backlog", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: self.open_new_window("Backlogged Video Games")
        )
        self.backlog_button.pack(side=ctk.LEFT, padx=30)

        self.wishlist_button = ctk.CTkButton(
            self.button_row, text="Wishlist", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: self.open_new_window("Wishlisted Video Games")
        )
        self.wishlist_button.pack(side=ctk.LEFT, padx=30)

    def update_stats(self):
        total_games = self.tracker.get_total_games()
        completed_percent = self.tracker.get_completed_percentage()
        total_hours = self.tracker.get_total_hours_played()

        # Update main stats
        self.games_count.configure(text=str(total_games))
        self.percent_completed.configure(text=f"{completed_percent}%")
        self.hours_count.configure(text=str(total_hours))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x1000")
        self.title("CCT211: Video Game Tracker")

        self.tracker = GameTracker()

        self.home_frame = HomeFrame(master=self, tracker=self.tracker, width=1100, height=700, fg_color="#334669",
                                    corner_radius=40)
        self.home_frame.place(relx=0.5, y=220, anchor="n")

    def refresh_stats(self):
        self.tracker.create_games()
        self.update_stats()  # Update

app = App()
my_ctk_font = ctk.CTkFont(family="Roboto", size=14, weight="bold")
app_title = ctk.CTkLabel(app, text="Video Game Tracker", font=VIDEO_GAME_TRACKER_FONT())
app_title.place(x=455, y=100)

ctk.set_appearance_mode("light")
app.mainloop()
