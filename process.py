import json

table = {}

with open("train.json", "r") as file:
    data = json.load(file)
    current_month = 1
    for item in data:
        if "currentMonth" in item:
            if not table.get(item["currentMonth"], False):
                table[item["currentMonth"]] = {"market_state": item}
            current_month = item["currentMonth"]
        if "player_id" in item:
            if not table[current_month].get(item["player_id"]):
                table[current_month][item["player_id"]] = []
            table[current_month][item["player_id"]].append(item)

print(table, file=open("cleaned.json", "w"))
