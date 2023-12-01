import aiohttp
import aiofiles
import aiofiles.os
import json
from utils.config import config

UNDRESS_TOKEN = config.undress


async def upload_image_and_get_task_id(input_file_path):
    async with aiohttp.ClientSession() as session:
        presign_url = 'https://enterprise.undress.app/api/v2/enterprise/presign'
        headers = {'Authorization': UNDRESS_TOKEN}
        async with session.post(presign_url, headers=headers) as response:
            text_response = await response.text()
            data = json.loads(text_response)

        upload_url = data['url']
        task_id = data['taskId']

        async with aiofiles.open(input_file_path, 'rb') as image_file:
            image_data = await image_file.read()
        await aiofiles.os.remove(input_file_path)
        headers = {'Content-Type': 'image/jpg'}
        await session.put(upload_url, headers=headers, data=image_data)

    return task_id


async def start_generation(task_id, mode, body_type):
    async with aiohttp.ClientSession() as session:
        generation_url = 'https://enterprise.undress.app/api/v2/enterprise/generate'
        headers = {'Authorization': UNDRESS_TOKEN}
        body = {'queue': 'free', 'inputId': task_id, "generationMode": mode, "bodyType": body_type}
        async with session.post(generation_url, headers=headers, json=body) as response:
            text_response = await response.text()
            data = json.loads(text_response)

    return data['ok']


async def check_status(task_id):
    async with aiohttp.ClientSession() as session:
        status_url = f'https://enterprise.undress.app/api/v2/enterprise/task_status?task={task_id}'
        headers = {'Authorization': UNDRESS_TOKEN}
        async with session.get(status_url, headers=headers) as response:
            text_response = await response.text()
            data = json.loads(text_response)
    return data

