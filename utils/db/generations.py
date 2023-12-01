from datetime import datetime, timedelta
from utils.db import db
from utils.db.models import Generation

generations_collection = db.generations


def get_generation_by_user_id(user_id):
    generation = generations_collection.find_one({"user_id": user_id})
    if generation:
        generation.pop('_id', None)
        return Generation(**generation)
    else:
        return None


def add_generation(user_id, status, mode, body_type):
    generation = {
        "user_id": user_id,
        "status": status['status'],
        "date": datetime.now().replace(microsecond=0),
        "input_url": status['inputUrl'],
        "result_url": status['resultUrl'],
        "mode": mode,
        "body_type": body_type
    }
    generations_collection.insert_one(generation)


def count_generations_today():
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    query = {
        "date": {"$gte": today_start, "$lt": today_end}
    }

    count_today = generations_collection.count_documents(query)
    return count_today
