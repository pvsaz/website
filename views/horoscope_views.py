from horoscope import Horoscope
from flask import Blueprint, request, render_template

pokemon_horoscope = Blueprint(
    "pokemon_horoscope", __name__, template_folder="templates", static_folder="static"
)


@pokemon_horoscope.route("/pokemon/sign", methods=["GET", "POST"])
def get_sign():
    if request.method == "POST":
        star_sign = request.form["star_sign"].lower()
        user_horoscope = Horoscope(star_sign)
        return have_sign(user_horoscope)
    else:
        return render_template("horo.html")


@pokemon_horoscope.route("/pokemon/show")
def have_sign(user_horoscope):
    return render_template(
        "showhoro.html",
        sign=user_horoscope.sign,
        horoscope=user_horoscope.horoscope,
        poke=user_horoscope.lucky_poke_name,
        pic=user_horoscope.lucky_poke_pic_url,
    )
