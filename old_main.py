import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from data import *
import os

logo_path = "pictures/homepage_logo.png"
open_logo = Image.open(logo_path)
tk_logo = customtkinter.CTkImage(open_logo, size=(190, 120))


def open_new_window(master, title):
    new_window = ctk.CTkToplevel(master)
    new_window.title(title)
    new_window.geometry("700x500")

    new_window.attributes("-topmost", True)


class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # ---------------- LABELS FOR GAME STATS ------------------

        self.your_stats = ctk.CTkLabel(self, text="Your Stats",
                                       font=("Arial", 36, "bold"),
                                       fg_color="#334669", text_color="white",
                                       anchor="w"
                                       )
        self.your_stats.place(relx=0.5, y=20, anchor="n")

        self.stats_row = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_row.place(relx=0.5, y=85, anchor="n")

        self.registered_games = ctk.CTkLabel(self.stats_row,
                                             text="Games Registered",
                                             font=("Arial", 22, "bold"),
                                             fg_color="#334669",
                                             text_color="white")
        self.registered_games.pack(side=ctk.LEFT, padx=55)

        self.per_completed = ctk.CTkLabel(self.stats_row, text="% Completed",
                                          font=("Arial", 22, "bold"),
                                          fg_color="#334669",
                                          text_color="white")
        self.per_completed.pack(side=ctk.LEFT, padx=55)

        self.num_hours_played = ctk.CTkLabel(self.stats_row,
                                             text="Hours Played",
                                             font=("Arial", 22, "bold"),
                                             fg_color="#334669",
                                             text_color="white")
        self.num_hours_played.pack(side=ctk.LEFT, padx=55)

        # --------------- LABEL FOR LIST BUTTONS ---------------------

        self.your_lists = ctk.CTkLabel(self, text="Your Lists",
                                       font=("Arial", 36, "bold"),
                                       fg_color="#334669", text_color="white",
                                       anchor="w")
        self.your_lists.place(relx=0.5, y=200, anchor="n")

        # --------------- BUTTONS FOR LIST PAGES -------------------

        self.button_row = ctk.CTkFrame(self, fg_color="transparent")
        self.button_row.place(relx=0.5, y=275, anchor="n")

        self.all_button = ctk.CTkButton(
            self.button_row, text="All", width=80, height=50,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 20, "bold"),
            command=lambda: open_new_window(self, "All Video Games")
        )
        self.all_button.pack(side=ctk.LEFT, padx=20)

        self.completed_button = ctk.CTkButton(
            self.button_row, text="Completed", width=90, height=50,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 20, "bold"),
            command=lambda: open_new_window(self, "Completed Video Games")
        )
        self.completed_button.pack(side=ctk.LEFT, padx=20)

        self.ongoing_button = ctk.CTkButton(
            self.button_row, text="Ongoing", width=90, height=50,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 20, "bold"),
            command=lambda: open_new_window(self, "Ongoing Video Games")
        )
        self.ongoing_button.pack(side=ctk.LEFT, padx=20)

        self.backlog_button = ctk.CTkButton(
            self.button_row, text="Backlog", width=90, height=50,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 20, "bold"),
            command=lambda: open_new_window(self, "Backlogged Video Games")
        )
        self.backlog_button.pack(side=ctk.LEFT, padx=20)

        self.wishlist_button = ctk.CTkButton(
            self.button_row, text="Wishlist", width=90, height=50,
            fg_color="#5F7DB0", hover_color="#3D63A1",
            corner_radius=15, text_color="white",
            font=("Arial", 20, "bold"),
            command=lambda: open_new_window(self, "Wishlisted Video Games")
        )
        self.wishlist_button.pack(side=ctk.LEFT, padx=20)


# --------- MAIN APP -> MASTER WINDOW -----------

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("CCT211: Video Game Tracker")

        self.home_frame = HomeFrame(master=self, width=750, height=400,
                                    fg_color="#334669", corner_radius=40)
        self.home_frame.place(relx=0.5, y=175, anchor="n")


app = App()

app_title = ctk.CTkLabel(app, text="Video Game Tracker",
                         font=("Arial", 50, "bold"))
app_title.place(x=270, y=60)

logo_label = ctk.CTkLabel(app, image=tk_logo, text="")
logo_label.place(x=40, y=40)


data = load_data()

ctk.set_appearance_mode("light")

app.mainloop()
