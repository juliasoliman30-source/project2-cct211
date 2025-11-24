import customtkinter as ctk
from PIL import Image
from data import *
from fonts import *
import os

class Game:
    def __init__(self, title, platform, status, rating=0, hours_played=0, imagePath=""):
        self.title = title
        self.platform = platform
        self.status = status  # "completed", "ongoing", "backlog", "wishlist"
        self.rating = rating
        self.hours_played = hours_played
        self.imagePath = imagePath


class GameTracker:
    def __init__(self, username="default_user"):
        self.username = username
        self.games = []
        self.csv_file = "games_data.csv"
        self.load_from_csv()

    def load_from_csv(self):
        """Load games from CSV file using data.py"""
        csv_data = load_data()
        for game_data in csv_data:
            # Convert CSV status to match your code
            status = self.normalize_status(game_data.get("Status", ""))

            game = Game(
                title=game_data.get("Title", ""),
                platform=game_data.get("Platform", ""),
                status=status,
                rating=int(game_data.get("Rating", 0)),
                hours_played=int(game_data.get("Hours", 0)),
                imagePath="pictures/" + game_data.get("ImagePath", "")
            )
            self.games.append(game)

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


class GameEntry(ctk.CTkFrame):
    def __init__(self, master, game, **kwargs):
        super().__init__(master, **kwargs)
        self.game = game
        self.configure(fg_color="#E8E8E8", corner_radius=8, height=60)

        self.setup_entry()

    def setup_entry(self):
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
        title_label = ctk.CTkLabel(title_frame, text=self.game.title,
                                   font=ENTRY_FONT(),
                                   text_color="#2C2C2C")
        title_label.pack(side=ctk.LEFT)
        status_color = self.get_status_color(self.game.status)
        status_frame = ctk.CTkFrame(self, fg_color=status_color,
                                    corner_radius=12, width=120, height=25)
        status_frame.grid(row=0, column=1, padx=20, pady=17)
        status_frame.grid_propagate(False)

        status_text = self.game.status.upper()
        if status_text == "WISHLIST":
            status_text = "WISHLISTED"

        status_label = ctk.CTkLabel(status_frame, text=status_text,
                                    font=ENTRY_FONT(),
                                    text_color="white")
        status_label.place(relx=0.5, rely=0.5, anchor="center")

        # Platform
        platform_label = ctk.CTkLabel(self, text=self.game.platform,
                                      font=ENTRY_FONT(),
                                      text_color="#2C2C2C")
        platform_label.grid(row=0, column=2, padx=20, pady=15, sticky="w")

        # Hours played
        hours_text = str(self.game.hours_played) if self.game.hours_played > 0 or self.game.status in ["ongoing", "completed"] else "--"
        hours_label = ctk.CTkLabel(self, text=hours_text,
                                   font=ENTRY_FONT(),
                                   text_color="#2C2C2C")
        hours_label.grid(row=0, column=3, padx=20, pady=15, sticky="w")

        # Action buttons
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=0, column=4, padx=20, pady=15, sticky="e")
        
        # edit button
        edit_img = Image.open("pictures/edit_icon.png")
        edit_icon = ctk.CTkImage(edit_img, size=(16, 16))
        edit_button = ctk.CTkButton(actions_frame, image=edit_icon, text="", width=16, height=16, fg_color="transparent", hover=False, command=self.edit_game)
        edit_button.pack(side=ctk.LEFT, padx=5)
        
        # delete button
        delete_img = Image.open("pictures/delete_icon.png")
        delete_icon = ctk.CTkImage(delete_img, size=(16, 16))
        delete_button = ctk.CTkButton(actions_frame, image=delete_icon, text="", width=16, height=16, fg_color="transparent", hover=False, command=self.delete_game)
        delete_button.pack(side=ctk.LEFT, padx=5)
    
    def assign_image_icon(self, parent, icon_path):
        if not icon_path or not os.path.exists(icon_path):
            icon_path = "pictures/defaultIcon.png"

        try:
            img = Image.open(icon_path)
        except Exception:
            img = Image.open("pictures/defaultIcon.png")

        icon_image = ctk.CTkImage(img, size=(30,30))
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
        print(f"Edit game: {self.game.title}") #placeholda
    
    def delete_game(self):
        """
        Pop up a Yes/No window to confirm the user's delete action.
        """
        print(f"Delete game: {self.game.title}") # palceholda


class ListPage(ctk.CTkFrame):
    def __init__(self, master, tracker, status, **kwargs):
        super().__init__(master, **kwargs)
        self.tracker = tracker
        self.status = status
        self.configure(fg_color="#334669")

        self.setup_ui()
        self.load_games()

    def setup_ui(self):
        # title Page 
        title_text = f"{self.status.upper()}" if self.status != "all" else "ALL GAMES"
        self.title_label = ctk.CTkLabel(self, text=title_text,
                                        font=("Arial", 48, "bold"),
                                        text_color="white")
        self.title_label.pack(pady=30)

        # Back button
        self.back_button = ctk.CTkButton(self, text="← Back to Home",
                                         width=200, height=40,
                                         fg_color="#5F7DB0", hover_color="#3D63A1",
                                         corner_radius=10, text_color="white",
                                         font=("Arial", 16, "bold"),
                                         command=self.master.show_home_page)
        self.back_button.pack(pady=20)

        # Table header
        self.create_table_header()

        # Scroll thingy for game entries
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=900)
        self.scrollable_frame.pack(fill="both", expand=True, padx=50, pady=10)

    def create_table_header(self):
        """Create the table header with column titles"""
        header_frame = ctk.CTkFrame(self, fg_color="#5F7DB0", corner_radius=8, height=50)
        header_frame.pack(fill="x", pady=(0, 10), padx=50)
        header_frame.pack_propagate(False)

        # Configure header grid columns
        header_frame.grid_columnconfigure(0, weight=2, minsize=300)  # Title
        header_frame.grid_columnconfigure(1, weight=1, minsize=150)  # Status
        header_frame.grid_columnconfigure(2, weight=1, minsize=150)  # Platform
        header_frame.grid_columnconfigure(3, weight=1, minsize=150)  # Hours Played

        # Header labels
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

    def load_games(self):
        """Load and display games as individual entries"""
        games = self.tracker.get_games_by_status(self.status)

        if not games:
            # Show empty state message
            empty_label = ctk.CTkLabel(self.scrollable_frame,
                                       text=f"No {self.status} games found.\nClick 'Add Game' to get started!",
                                       font=("Arial", 24),
                                       text_color="white")
            empty_label.pack(pady=50)
            return

        # Display each game as an individual entry
        for game in games:
            entry = GameEntry(self.scrollable_frame, game)
            entry.pack(fill="x", pady=5, padx=10)


def open_new_window(master, title):
    new_window = ctk.CTkToplevel(master)
    new_window.title(title)
    new_window.geometry("1200x1000")
    new_window.configure(fg_color="#334669")

    # Extract status from title 
    status_map = {
        "All Video Games": "all",
        "Completed Video Games": "completed",
        "Ongoing Video Games": "ongoing",
        "Backlogged Video Games": "backlog",
        "Wishlisted Video Games": "wishlist"
    }
    status = status_map.get(title, "all")

    # tracker and load data
    tracker = GameTracker()

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

    # Scrollable thingy 
    scrollable_frame = ctk.CTkScrollableFrame(new_window, fg_color="transparent", width=900)
    scrollable_frame.pack(fill="both", expand=True, padx=50, pady=10)

    # 
    games = tracker.get_games_by_status(status)

    if not games:
        # Show empty state message
        empty_label = ctk.CTkLabel(scrollable_frame,
                                   text=f"No {status} games found.\nClick 'Add Game' to get started!",
                                   font=("Arial", 24),
                                   text_color="white")
        empty_label.pack(pady=50)
    else:
        # entry display
        for game in games:
            entry = GameEntry(scrollable_frame, game)
            # entry.pack(fill="x", pady=5, padx=10)
            entry.pack(fill="x", pady=5)


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.your_stats = ctk.CTkLabel(self, text="Your Stats",
                                       font=HOME_FRAME_LARGE_FONT(),
                                       fg_color="#334669", text_color="white",
                                       anchor="w"
                                       )
        self.your_stats.place(relx=0.5, y=30, anchor="n")

        self.your_lists = ctk.CTkLabel(self, text="Your Lists",
                                       font=HOME_FRAME_LARGE_FONT(),
                                       fg_color="#334669", text_color="white",
                                       anchor="w")
        self.your_lists.place(relx=0.5, y=475, anchor="n")

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

        self.button_row = ctk.CTkFrame(self, fg_color="transparent")
        self.button_row.place(relx=0.5, y=570, anchor="n")

        self.all_button = ctk.CTkButton(
            self.button_row, text="All", width=100, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: open_new_window(self, "All Video Games")
        )
        self.all_button.pack(side=ctk.LEFT, padx=30)

        self.completed_button = ctk.CTkButton(
            self.button_row, text="Completed", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: open_new_window(self, "Completed Video Games")
        )
        self.completed_button.pack(side=ctk.LEFT, padx=30)

        self.ongoing_button = ctk.CTkButton(
            self.button_row, text="Ongoing", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: open_new_window(self, "Ongoing Video Games")
        )
        self.ongoing_button.pack(side=ctk.LEFT, padx=30)

        self.backlog_button = ctk.CTkButton(
            self.button_row, text="Backlog", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: open_new_window(self, "Backlogged Video Games")
        )
        self.backlog_button.pack(side=ctk.LEFT, padx=30)

        self.wishlist_button = ctk.CTkButton(
            self.button_row, text="Wishlist", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=HOME_FRAME_SMALL_FONT(),
            command=lambda: open_new_window(self, "Wishlisted Video Games")
        )
        self.wishlist_button.pack(side=ctk.LEFT, padx=30)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x1000")
        self.title("CCT211: Video Game Tracker")

        self.home_frame = HomeFrame(master=self, width=1100, height=700,
                                    fg_color="#334669", corner_radius=40)
        self.home_frame.place(relx=0.5, y=220, anchor="n")


app = App()
my_ctk_font = ctk.CTkFont(family="Roboto", size=14, weight="bold")
app_title = ctk.CTkLabel(app, text="Video Game Tracker", font=VIDEO_GAME_TRACKER_FONT())
app_title.place(x=455, y=100)

ctk.set_appearance_mode("light")
app.mainloop()
