import uuid

import json
import random

# ELO constants
K = 32
DEFAULT_RATING = 1600

# JSON file to store player ratings
RATING_FILE = "json/candidates1.json_promises.json"


def get_ratings():
    """
    Reads the JSON file and returns a dictionary of player ratings.
    If the file does not exist, creates an empty dictionary and returns it.
    """
    try:
        with open(RATING_FILE, "r", encoding="utf-8") as f:
            ratings = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        ratings = {}
    return ratings


def save_ratings(ratings):
    """
    Writes the given ratings dictionary to the JSON file.
    """
    with open(RATING_FILE, "w") as f:
        json.dump(ratings, f)


def select_players(ratings, rating_range=400):
    """
    Randomly selects two players from the given list of players that have similar ratings.
    Returns a tuple of the selected players.
    """
    # sort players by rating
    sorted_ratings = sorted(ratings, key=lambda x: x["ranking"])
    # get random player
    player1 = random.choice(sorted_ratings)
    # filter players with similar ratings
    similar_players = [player for player in sorted_ratings if
                       abs(player["ranking"] - player1["ranking"]) <= rating_range]
    # get random player from similar players
    player2 = random.choice(similar_players)

    return player1, player2


def update_ratings(winner, loser, ratings):
    """
    Updates the ELO ratings of the given winner and loser and saves the updated ratings to the JSON file.
    """
    winner_expected = 1 / (1 + 10 ** ((loser["ranking"] - winner["ranking"]) / 400))
    loser_expected = 1 / (1 + 10 ** ((winner["ranking"] - loser["ranking"]) / 400))

    # find the winner in the ratings list and update their rating
    for player in ratings:
        if player["id"] == winner["id"]:
            player["ranking"] = winner["ranking"] + K * (1 - winner_expected)
            break
    # find the loser in the ratings list and update their rating
    for player in ratings:
        if player["id"] == loser["id"]:
            player["ranking"] = loser["ranking"] + K * (0 - loser_expected)
            break
    save_ratings(ratings)


def new_match():
    """
    Creates a random UUID to use as an identifier for a new match.
    """
    s = str(uuid.uuid4())
    p1, p2 = select_players(get_ratings())
    match = {"id": s, "player_1": p1, "player_2": p2}
    with open("matches.json", "a") as f:
        f.write(s + "\n")
    return s


def main():
    ratings = get_ratings()
    p1, p2 = select_players(ratings)
    if p1["id"] == p2["id"]:
        return
    if len(p1["promises"]) == 0 or len(p2["promises"]) == 0:
        return

    winner = ""
    while winner not in ["1", "2"]:
        winner = input(f"Choose winner:\n1: {random.choice(p1['promises'])}\n2: {random.choice(p2['promises'])}\n")

    if winner == "1":
        winner = p1
        loser = p2
    else:
        winner = p2
        loser = p1

    # print(f"{winner} wins! {loser} loses.")
    update_ratings(winner, loser, ratings)


if __name__ == "__main__":
    while True:
        main()
