# Flik scraping script

# python imports
import json, requests


def get_flik_url(type, year, month, day) -> str:
    return f"https://hackleyschool.flikisdining.com/menu/api/weeks/school/hackley-school/menu-type/{type}/{year}/{month}/{day}/"

def parse_header(header) -> str:
    header_value = header["text"].encode().decode('utf-8')
    return header_value

def parse_food(food) -> dict:
    name = food["name"]

    try:
        nutrition = food["rounded_nutrition_info"]
    except:
        nutrition = None

    ingredients = food["ingredients"]

    try:
        serving_size = food["serving_size_info"]
    except:
        serving_size = None

    food_item = {
        "name": name,
        "nutrition": nutrition,
        "ingredients": ingredients,
        "serving_size": serving_size
    }
    
    return food_item

def parse_meal(meal) -> dict:
    
    meal = json.loads(meal)

    days_list = meal["days"]

    menu = {}

    for day in days_list:
        day_menu = {}

        date = day["date"]
        day_menu["date"] = date

        food_items = []
        menu_items = day["menu_items"]
        for menu_item in menu_items:

            current_header = None

            if menu_item["food"] is not None:
                food = parse_food(menu_item["food"])
                header = current_header
            else: 
                food = None
                header = parse_header(menu_item)
                current_header = header

            if food is not None:
                food_items.append(food)

        day_menu["food"] = food_items

        menu[date] = day_menu
    
    return menu

def parse_menu(breakfast, lunch, dinner) -> dict:

    menu = {}

    breakfast = parse_meal(breakfast)
    lunch = parse_meal(lunch)
    dinner = parse_meal(dinner)

    for date in breakfast:
        menu[date] = {
            "breakfast": breakfast[date],
            "lunch": lunch[date],
            "dinner": dinner[date]
        }

    return menu

def get_flik_data(type, day, month, year) -> str:

    # request for data
    url = get_flik_url(type, year, month, day)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    response_text = response.text

    # log data
    #file = open("logs/menu.json", "a")
    #file.write(response_text)
    #file.close()

    return response_text

def scrape_flik(day, month, year) -> dict:

    breakfast = get_flik_data("breakfast", day, month, year)
    lunch = get_flik_data("lunch", day, month, year)
    dinner = get_flik_data("dinner", day, month, year)

    menu = parse_menu(breakfast, lunch, dinner)

    return menu



    







