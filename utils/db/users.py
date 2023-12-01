from datetime import datetime, timedelta
from utils.db import db
from utils.db.models import User

users_collection = db.users


def get_user_db(user_id):
    user = users_collection.find_one({"user_id": user_id})
    if user:
        user.pop('_id', None)
        return User(**user)
    else:
        return None


def add_user(user, ref_code):
    user = {
            "user_id": user.id,
            "username": user.username,
            "lang": user.language_code,
            "reg_date": datetime.now().replace(microsecond=0),
            "gen_avail": 0,
            "gen_done": 0,
            "gen_trial": 1,
            "ref_code": ref_code,
            "refs": 0
        }
    users_collection.insert_one(user)
    user.pop('_id', None)
    return User(**user)


def update_data_user(user_id, new_data):
    filter_criteria = {"user_id": user_id}
    update_data = {"$set": new_data}
    users_collection.update_one(filter_criteria, update_data)


def update_gens(user_id, gens, amount):
    user = users_collection.find_one({"user_id": user_id})
    current_gen_avail = user[gens]
    update_data_user(user_id, {gens: current_gen_avail + amount})


def update_ref(user_id):
    user = users_collection.find_one({"user_id": user_id})
    current_refs = user['refs']
    update_data_user(user_id, {"refs": current_refs + 1})


def update_lang(user_id, lang):
    update_data_user(user_id, {"lang": lang})


def count_users_today():
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    query = {
        "reg_date": {"$gte": today_start, "$lt": today_end}
    }

    count_today = users_collection.count_documents(query)
    return count_today
