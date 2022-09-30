# Purna Shah's Portfolio 
## Running at [shah.codes](http://shah.codes)
### Introduction
Built with:
- Backend in Flask and SQLAlchemy
- Frontend in Bootstrap CSS/HTML
- CI/CD pipeline between Github and Docker using Github Actions
- Running in prod with AWS Elastic Beanstalk
\
\
One section of the website is a blogging app with full CRUD capabilities and account management. All posts can be seen without an account, but an account must be made to post. User must be logged in with the correct account to delete corresponding posts. Lastly, the account and all associated posts can be deleted with the press of a button in the user's profile. Inspired by [this](https://www.youtube.com/watch?v=3mwFC4SHY-Y) Youtube how-to and [this](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login) tutorial. Please see the below ~minute-long GIF for a demonstration of this.
\
\
![](https://github.com/pvsaz/projects/blob/main/demo.gif)
\
\
The other section of the website (Pokémon-Horoscope Fun!) arose from an idea to chain public APIs ([aztro API](https://aztro.sameerkumar.website/) and [PokéAPI](https://pokeapi.co/)) in a custom class and store the information together in an object.
### Code Explanation
The main script that initializes and runs the website is app.py. /static and /templates house CSS and HTML files. I use Flask's blueprints feature to separate the views from app.py and store them in a package in /views. The custom class used in the horoscope feature lives in horoscope.py. Lastly, database.py is used to detach the database object from app.py so it can be used both in /views and app.py without circular imports.
