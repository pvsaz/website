import requests
from datetime import datetime
import re

class Horoscope:
    def __init__(self, sign, day='today'):
        self.sign = sign
        self.day = day
        self.horoscope = self.get_horoscope()
        self.lucky_number = self.get_lucky_number()
        self.lucky_poke_name = self.get_poke_name()
        self.lucky_poke_pic_url = self.get_poke_img_url()

    def get_horoscope(self):
        params = (('sign', self.sign), ('day', self.day))
        result = requests.post('https://aztro.sameerkumar.website/', params=params)
        return result.json()['description']
    
    def get_lucky_number(self):
        params = (('sign', self.sign), ('day', self.day))
        result = requests.post('https://aztro.sameerkumar.website/', params=params)
        if int(result.json()['lucky_number']) > 890 or int(result.json()['lucky_number']) < 1:
            # dont query PokeAPI if PokeDex ID does not exist (at time of writing)
            return str(890)
        return result.json()['lucky_number']

    def get_poke_name(self):
        result = requests.get('https://pokeapi.co/api/v2/pokemon/' + self.lucky_number)
        return result.json()['name']

    def get_poke_img_url(self):
        result = requests.get('https://pokeapi.co/api/v2/pokemon/' + self.lucky_number)
        return result.json()['sprites']['front_default']