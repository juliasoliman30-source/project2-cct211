import csv, os, random, string

CSV_PATH = os.path.join(os.path.dirname(__file__), "GameSampleData.csv")

def load_data():
    """
    Reads a CSV file and returns its content as a list of dictionaries.

    So if the data looked like:
    Title       Status      Platform    Hours   Ratings
    Minecraft   Ongoing     PC          48      4
    Zelda       Completed   Switch      85      5
    Mario       Ongoing     Switch      40      3

    The returned data from this function would look like:
    [
        {
            Title: "Minecraft",
            Status: "Ongoing",
            Platform: "PC",
            Hours: "48",
            Ratings: "4"
        },
        {
            Title: "Zelda",
            Status: "Completed",
            Platform: "Switch",
            Hours: "85",
            Ratings: "5"
        },
        {
            Title: "Mario",
            Status: "Completed",
            Platform: "Switch",
            Hours: "40",
            Ratings: "3"
        }
    ]
    """
    dicts = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
            dicts = list(csv.DictReader(f))
    return dicts

def write_data_to_csv(data):
    """
    Writes the given data to the csv file.
    """
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Title", "Platform", "Status", "Hours", "Rating", "ImagePath"])
        writer.writeheader()
        writer.writerows(data)

def generate_unique_id(data):
    """
    Generates a random unique ID consisting of 3 uppercase letters followed by 3 digits.

    For example: "BHE241", "ORE293", "ERE921" etc.
    """
    existing_ids = {row.get("ID") for row in data}

    while True:
        letters = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        newId = letters + digits
        if newId not in existing_ids:
             return newId
    