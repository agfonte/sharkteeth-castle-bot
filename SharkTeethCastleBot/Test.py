from pymongo import collection
import os, pymongo, logging

client = pymongo.MongoClient("mongodb+srv://admin:xBUdtcN1XaapnfBL@cluster0.j0ylo.azure.mongodb.net")
db = client["castle_debug"]
permissions = db["permissions"]

commander = permissions.find_one({"_id": "COMMANDERS"}, {"list"})["list"]
print(commander)

heroes = db["hero"]
userid = 387393551

# result = db.heros.update_one({"_id":userid}, {
#             "$set":{
#                 "squad": ""
#             }
#         })


# print(result)

leviatas =  heroes.find_one({"_id": userid})

print(leviatas)

# Inserts 
# commander_permissions = {
#     "_id": "COMMANDERS",
#     "priority": 0,
#     "list": [387393551]}
# id_inserted_data = permissions.insert_one(commander_permissions).inserted_id
# print(id_inserted_data)