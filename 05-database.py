import pickle
import sqlite3

import pandas as pd
from fire import Fire

con = sqlite3.connect("data/basketball.db")

with open("pickles/pipe.pkl", "rb") as f:
    pipe = pickle.load(f)


def fetch_player_data(name):
    player = pd.read_sql(
        f"""
        select
        *
        from players
        where name = '{name}'
        order by date desc
        limit 2
        """,
        con,
    ).sort_values("date", ascending=False)
    return player


def prep_data(player):
    X_new = pd.DataFrame(
        {
            "position": [player.position[0]],
            "points_1": [player.points[0]],
            "points_2": [player.points[1]],
        }
    )
    return X_new


def predict(player):
    X = fetch_player_data(player)
    date = X["date"].max()
    X = prep_data(X)
    points = round(pipe.predict(X)[0], 2)
    df = pd.DataFrame(
        {
            "date_created": pd.Timestamp("now"),
            "name": [player],
            "last_game": [date],
            "points": [points],
        }
    )
    df.to_sql("predictions", con, if_exists="append", index=False)
    print("Success!")


if __name__ == "__main__":
    Fire(predict)
