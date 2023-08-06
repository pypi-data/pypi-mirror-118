#!/bin/python

import os
import typer
import time
import json
import requests 
import typer

app = typer.Typer()

objectives = {
    "lose": "lose_fat",
    "maintain": "maintain_weight",
    "gain": "build_muscle"
}


def edit_nutrition_preferences(session, objective, number_of_meals_per_days):
    url = "http://localhost:8000/api/v1/user/edit_nutrition_preferences/"
    headers = {'Content-Type': 'application/json', "X-CSRF-TOKEN": session.cookies['csrf_access_token']}
    payload = {"objective":objective, "number_of_meals_per_days": number_of_meals_per_days}

    assert objective in ["maintain_weight", "build_muscle", "lose_fat"]
    assert number_of_meals_per_days >= 3 and number_of_meals_per_days <= 6
    resp = session.put(url, headers=headers, data=json.dumps(payload,indent=4))

    return resp.json()


def get_user(session):
    resp = session.get("http://localhost:8000/api/v1/user/")
    json_data = resp.json()

    return resp.json()


def get_meals(session):
    resp = session.get("http://localhost:8000/api/v1/meals")
    json_data = resp.json()

    return resp.json()


def update_user(session, weight, objective, number_of_meals_per_days):
    url = 'http://localhost:8000/api/v1/meals/update_meal_plan/'
    headers = {'Content-Type': 'application/json', "X-CSRF-TOKEN": session.cookies['csrf_access_token']}
    payload = {"weight":weight, "objective":objective, "number_of_meals_per_days": number_of_meals_per_days}

    assert objective in ["maintain_weight", "build_muscle", "lose_fat"]
    assert number_of_meals_per_days >= 3 and number_of_meals_per_days <= 6
    resp = session.post(url, headers=headers, data=json.dumps(payload,indent=4))

    return resp.json()

    
def onboard(session):
    url = 'http://localhost:8000/api/v1/user/onboarding/'
    headers = {'Content-Type': 'application/json', "X-CSRF-TOKEN": session.cookies['csrf_access_token']}
    payload = {"activity_level":"sedentary", "gender":"male", "height":180, "weight":80, "objective":"maintain_weight", "number_of_meals_per_days": 6, "birth_date": "2002-07-18"}

    resp = session.post(url, headers=headers, data=json.dumps(payload,indent=4))

    return resp.json()


def get_grocery_list(session, days):
    url = 'http://localhost:8000/api/v1/meals/grocery_list/'
    headers = {'Content-Type': 'application/json', "X-CSRF-TOKEN": session.cookies['csrf_access_token']}
    timestamps = []
    current_time = int(time.time())
    for i in range(days):
        current_time_plus_N_days = current_time + i * 24 * 3600
        timestamps.append(current_time_plus_N_days)
        
    payload = {"timestamps": timestamps}
 
    resp = session.post(url, headers=headers, data=json.dumps(payload,indent=4))
    return resp.json()



def ensure_nutrimium_directory_exists():
    directory = ".nutrimium"
    parent_dir = f'/home/{os.environ.get("USER")}'
    path = os.path.join(parent_dir, directory)

    if not os.path.isdir(path):
        os.mkdir(path)
    

def save_cookies(session):
    with open(f'/home/{os.environ.get("USER")}/.nutrimium/credentials', 'w') as outfile:
        json.dump(dict(session.cookies), outfile)


def get_session():
    session = requests.Session()
    with open(f'/home/{os.environ.get("USER")}/.nutrimium/credentials', 'r') as infile:
        try:
            cookies = json.load(infile)
        except:
            cookies = {}
    session.cookies = requests.cookies.cookiejar_from_dict(cookies)
    return session


def _login(use_cache=True):
    session = get_session()
    if 'access_token_cookie' not in session.cookies.keys() or not use_cache:
        identity = typer.prompt("What's your email?")
        password = typer.prompt("What's your password?", hide_input=True)
        session = requests.Session()

        url = 'http://localhost:8000/api/auth/'
        headers = {'Content-Type': 'application/json'}
        payload = {'identity': f'{identity}', 'password': f'{password}'}
        resp = session.post(url, headers=headers, data=json.dumps(payload,indent=4))

        if resp.status_code == 200:
            save_cookies(session)
        else:
            raise Exception("Error while trying to log in")

    return session



def handle_errors(response):
    if "error" in response.keys():
        error = response["error"]
        message = error["message"]
        if message == "Your auth token has expired":
            return "You need to login again, type: nutrimium login"

    return None


def run_command(func, *args, **kwargs):
    session = _login()
    response = func(session, *args, **kwargs)
    message = handle_errors(response)
    if message is not None:
        print(message)
    else:
        print(json.dumps(response))


@app.command()
def login():
    ensure_nutrimium_directory_exists()
    _login(use_cache=False)

@app.command()
def user():
    run_command(get_user)

@app.command()
def update():
    weight = typer.prompt("What's your weight in kilograms?")
    while True:
        try:
            assert "." not in weight # prevent floats
            meals = int(weight) # prevent not integers
            break
        except:
            weight = typer.prompt("What's your weight in kilograms?")

    
    objective = typer.prompt("What's your objective? Choose from: lose|maintain|gain")
    while objective not in ["lose", "maintain", "gain"]:
        objective = typer.prompt("Your objective must be lose, maintain or gain. What's your objective?")

    meals = typer.prompt("How many meals do you want per day?")
    while True:
        try:
            assert "." not in meals # prevent floats
            meals = int(meals) # prevent not integers
            assert meals >= 3
            assert meals <= 6
            break
        except:
            meals = typer.prompt("You should choose a value between 3 and 6 (both included). How many meals do you want per day?")
            
    run_command(update_user, weight=weight, objective=objectives[objective], number_of_meals_per_days=meals)

@app.command()
def meals():
    run_command(get_meals)

@app.command()
def groceries(
        days: int = typer.Option(3, min=1, max=7),
        help="The number of days to include in the grocery list."
):
    run_command(get_grocery_list, days=days)

@app.command()
def edit(
    help="Edit nutrition preferences."
):

    objective = typer.prompt("What's your objective? Choose from: lose|maintain|gain")
    while objective not in ["lose", "maintain", "gain"]:
        objective = typer.prompt("Your objective must be lose, maintain or gain. What's your objective?")

    meals = typer.prompt("How many meals do you want per day?")
    while True:
        try:
            assert "." not in meals # prevent floats
            meals = int(meals) # prevent not integers
            assert meals >= 3
            assert meals <= 6
            break
        except:
            meals = typer.prompt("You should choose a value between 3 and 6 (both included). How many meals do you want per day?")
        
    run_command(edit_nutrition_preferences, objective=objectives[objective], number_of_meals_per_days=meals)
    

    
if __name__ == "__main__":
    app()
