import customtkinter as ctk
from PIL import Image
from data import *


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.your_stats = ctk.CTkLabel(self, text="Your Stats",
                                       font=("Arial", 48, "bold"),
                                       fg_color="#334669", text_color="white",
                                       anchor="w"
                                       )
        self.your_stats.place(relx=0.5, y=30, anchor="n")

        self.your_lists = ctk.CTkLabel(self, text="Your Lists",
                                       font=("Arial", 48, "bold"),
                                       fg_color="#334669", text_color="white",
                                       anchor="w")
        self.your_lists.place(relx=0.5, y=475, anchor="n")

        self.stats_row = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_row.place(relx=0.5, y=125, anchor="n")

        self.registered_games = ctk.CTkLabel(self.stats_row,
                                             text="Games Registered",
                                             font=("Arial", 22, "bold"),
                                             fg_color="#334669",
                                             text_color="white")
        self.registered_games.pack(side=ctk.LEFT, padx=70)

        self.per_completed = ctk.CTkLabel(self.stats_row, text="% Completed",
                                          font=("Arial", 22, "bold"),
                                          fg_color="#334669",
                                          text_color="white")
        self.per_completed.pack(side=ctk.LEFT, padx=70)

        self.num_hours_played = ctk.CTkLabel(self.stats_row,
                                             text="Hours Played",
                                             font=("Arial", 22, "bold"),
                                             fg_color="#334669",
                                             text_color="white")
        self.num_hours_played.pack(side=ctk.LEFT, padx=70)

        self.button_row = ctk.CTkFrame(self, fg_color="transparent")
        self.button_row.place(relx=0.5, y=570, anchor="n")

        self.all_button = ctk.CTkButton(
            self.button_row, text="All", width=100, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 24, "bold")
        )
        self.all_button.pack(side=ctk.LEFT, padx=30)

        self.completed_button = ctk.CTkButton(
            self.button_row, text="Completed", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 24, "bold")
        )
        self.completed_button.pack(side=ctk.LEFT, padx=30)

        self.ongoing_button = ctk.CTkButton(
            self.button_row, text="Ongoing", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 24, "bold")
        )
        self.ongoing_button.pack(side=ctk.LEFT, padx=30)

        self.backlog_button = ctk.CTkButton(
            self.button_row, text="Backlog", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 24, "bold")
        )
        self.backlog_button.pack(side=ctk.LEFT, padx=30)

        self.wishlist_button = ctk.CTkButton(
            self.button_row, text="Wishlist", width=90, height=70,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 24, "bold")
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

app_title = ctk.CTkLabel(app, text="Video Game Tracker",
                         font=("Arial", 70, "bold"))
app_title.place(x=455, y=100)
data = load_data()

ctk.set_appearance_mode("light")
app.mainloop()
