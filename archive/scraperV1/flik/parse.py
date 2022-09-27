""" import json

def parse_header(header):
    header_value = header["text"].encode().decode('utf-8')
    return header_value

def parse_food(food):
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

def parse_meal(meal):
    
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

def parse_menu(breakfast, lunch, dinner):

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






 """