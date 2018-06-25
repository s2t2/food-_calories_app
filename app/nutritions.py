from nutritionix import Nutritionix
import csv
from dotenv import load_dotenv
import json
import os
import pdb
import requests
import datetime

def write_prices_to_file(foods = [], filename="data/food.csv"):
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["item_name","calories"])
        writer.writeheader()
        for d in foods:
            row = {
                "item_name": d["item_name"], # change attribute name to match project requirements
                "calories": d["calories"]
            }
            writer.writerow(row)

if __name__ == '__main__':
    while True:
        gender = input("Is a male or female: ").lower()
        if gender not in "male" "female":
            print("Check Your Spelling. Expecting 'Male' or 'Female'")
            continue
        else:
            break

    while True:
        try:
            weight = int(input("Please input your weight(in pond): "))
        except ValueError:
            print("Sorry, Please Input Number.")
            continue
        if weight < 0:
                print("Sorry, your response must not be negative.")
                continue
        else:
            break

    while True:
        try:
            height = float(input("Please input your height(in feet): "))
        except ValueError:
            print("Sorry, Please Input Number.")
            continue
        if height < 0:
                print("Sorry, your response must not be negative.")
                continue
        else:
            break

    while True:
        try:
            age = int(input("Please input your age(eg.25): "))
        except ValueError:
            print("Sorry, Please Input Integer.")
            continue
        if age < 0:
                print("Sorry, your response must not be negative.")
                continue
        else:
            break

    print("----------------------------------------------------------------")
    print("Today is ", datetime.datetime.now().strftime("%Y-%B-%d"))
    print("Today's Food For You: ")

    if gender == "male":
        need_calories = (10 * weight * 0.4536 + 6.25 * height *30.48 - 5 * age + 5) * 1.2
    elif gender == "female":
        need_calories = (10 * weight * 0.4536 + 6.25 * height *30.48 - 5 * age - 161) * 1.2


    nix = Nutritionix(app_id="your_app_id", api_key="your_api_key")

    obj = nix.search().nxql(
        filters={
            "nf_calories": {
                #"lte": 500
                "from":200,
                "to":500
            }
        },
        fields=["item_name", "nf_calories"]).json()


    results = []
    for food in obj['hits']:
        result = {
                "item_name": food['fields']['item_name'],
                "calories": food['fields']['nf_calories']
        }
        results.append(result)

    #pdb.set_trace()
    filter_results = []
    total_calories = 0
    for result in results:
        total_calories += result["calories"]
        if total_calories <= need_calories:
            filter_results.append(result)
            print("Food Name: " + result['item_name'] + "........" + "Calroies: " + str(result['calories']))

    print("----------------------------------------------------------------")
    print("Have A Nice Day. Enjoy Your Meal.")

    food_calories = filter_results

    write_prices_to_file(foods = food_calories, filename="data/food.csv")
