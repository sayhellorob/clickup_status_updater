import os
import requests
import datetime
import logging
import time

# Wait for 1 second
time.sleep(1)

# log results
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Define your ClickUp API key and list ID
    API_KEY = os.environ['CLICKUP_API_KEY']
    LIST_ID = os.environ['CLICKUP_TASK_LIST_ID']
    CUSTOM_DATE_FIELD_ID = os.environ['CLICKUP_CUSTOM_DATE_FIELD_ID']

    # Define the URL for retrieving the tasks in the list
    TASKS_URL = f'https://api.clickup.com/api/v2/list/{LIST_ID}/task'

    # Define the headers for the API requests
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }

    # Define the current date
    today = datetime.date.today()

    # Define the payload for the update requests
    payload = {
        'status': 'In Progress'
    }

    # Define the payload for the delete requests
    delete_payload = {
        'value': ''
    }

    # Retrieve the tasks in the list
    response = requests.get(TASKS_URL, headers=headers)
    tasks = response.json()['tasks']

    # Loop through the tasks and update the status if the custom date field is equal or less than today's date
    for task in tasks:
        task_id = task['id']
        status = task['status']['status']
        if status != 'closed' or status != 'in progress':
            custom_fields = task['custom_fields']
            date_value = None
            for field in custom_fields:
                if field['id'] == CLICKUP_CUSTOM_DATE_FIELD_ID:
                    date_value = field.get('value')
                    field_id = field['id']
                    break
            if date_value is not None:
                # Convert the Unix timestamp to a datetime object
                date_value = datetime.datetime.fromtimestamp(int(date_value) / 1000).date()
                if date_value <= today:
                    # Update the status of the task
                    update_url = f'https://api.clickup.com/api/v2/task/{task_id}'
                    response = requests.put(update_url, headers=headers, json=payload)
                    if response.status_code == 200:
                        logger.info(f'Task {task_id} updated successfully')
                    else:
                        logger.error(f'Error updating task {task_id}: {response.json()}')
                    # Delete the custom field value
                    delete_url = f'https://api.clickup.com/api/v2/task/{task_id}/field/{field_id}'
                    response = requests.delete(delete_url, headers=headers, json=delete_payload)
                    if response.status_code == 204:
                        logger.info(f'Task {task_id} field {field_id} deleted successfully')
                    else:
                        logger.error(f'Error deleting task {task_id} field {field_id}: {response.json()}')
    return {
        'statusCode': 200,
        'body': 'Success'
    }
