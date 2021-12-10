import requests
import time

link = 'https://playground.learnqa.ru/ajax/api/longtime_job'

start_tasks = requests.request('GET', link).json()
token = start_tasks['token']
seconds = start_tasks['seconds']

method_data = {
    'token': token
}

request_before_end__of_job = requests.request('GET', link, params=method_data).json()
print(f'Status: {request_before_end__of_job["status"]}')
print(f'Waiting {seconds} sec for ending job')
for i in range(1, seconds + 1):
    print(f'{i}...')
    time.sleep(1)

request_after_end_of_job = requests.request('GET', link, params=method_data).json()
print(f'Status: {request_after_end_of_job["status"]} / Results: {request_after_end_of_job["result"]}')
