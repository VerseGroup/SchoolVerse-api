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

menu = []

def parse_menu(json):
    days_list = json["days"]

    for day in days_list:
        day_menu = {}

        date = day["date"]
        day_menu["date"] = date

        food_items = []
        menu_items = day["menu_items"]
        for menu_item in menu_items:

            current_header = None

            if menu_item["food"] is not None:
                print('reached')
                food = parse_food(menu_item["food"])
                header = current_header
            else: 
                food = None
                header = parse_header(menu_item)
                current_header = header

            if food is not None:
                food_items.append(food)

        day_menu["food"] = food_items
    
        menu.append(day_menu)
    return menu


