import requests
import time

link = 'https://playground.learnqa.ru/ajax/api/longtime_job'

start_tasks = requests.request('GET', link).json()
time_starts = time.time()
token = start_tasks['token']
seconds = start_tasks['seconds']
print(f'Job is created. After {seconds} sec you can get the result')
time.sleep(1)

method_data = {
    'token': token
}

request_before_end__of_job = requests.request('GET', link, params=method_data).json()
print(f'You sent your request too early. Status Job: {request_before_end__of_job["status"]}')
time_before_end = time.time()
time_left = int(seconds - (time_before_end - time_starts))
print(f'You must waiting {time_left} sec to get the results')
for i in range(1, time_left + 1):
    print(f'{i}...')
    time.sleep(1)
print('Time is left, you can make your requests')
time.sleep(0.5)
request_after_end_of_job = requests.request('GET', link, params=method_data).json()
print(f'You make a request. Status Job: {request_after_end_of_job["status"]} / Results: {request_after_end_of_job["result"]}')
