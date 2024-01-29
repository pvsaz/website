import requests
from datetime import datetime
import re
import pandas as pd
import random

df = pd.read_csv("horoscope_data.csv")

class Horoscope:
    def __init__(self, sign, day="today"):
        self.sign = sign
        self.day = day
        self.horoscope = self.get_horoscope().lower()
        self.lucky_number = self.get_lucky_number()
        self.lucky_poke_name = self.get_poke_name()
        self.lucky_poke_pic_url = self.get_poke_img_url()

    def get_horoscope(self):
        description=df.loc[df['sign'] == self.sign, "description"].tolist()
        return random.choice(description)

    def get_lucky_number(self):
        lucky_numbers = df.loc[df['sign'] == self.sign, "lucky_number"].tolist()
        lucky_number = random.choice(lucky_numbers)
        if (
            lucky_number > 890
            or lucky_number < 1
        ):
            # dont query PokeAPI if PokeDex ID does not exist (at time of writing)
            return str(890)
        return str(lucky_number)

    def get_poke_name(self):
        result = requests.get("https://pokeapi.co/api/v2/pokemon/" + self.lucky_number)
        return result.json()["name"]

    def get_poke_img_url(self):
        result = requests.get("https://pokeapi.co/api/v2/pokemon/" + self.lucky_number)
        return result.json()["sprites"]["front_default"]
