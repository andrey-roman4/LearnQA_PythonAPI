import requests

link = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
list_with_methods = ['POST', 'PUT', 'DELETE', 'GET']
methods_out_of_list = ['HEAD', 'PATCH', 'OPTIONS']

def requests_whithout_any_params(url, list_methods):
    print('Запускаем цикл по сценарию когда тип метода не передается')
    for method_value in list_methods:
        response = requests.request(method_value, url)
        print(f'{method_value} - {response.text}')

def requests_out_of_lists(url, list_methods):
    print('Запускаем цикл по сценарию когда тип не из списака')
    for method_value in list_methods:
        method_data = {
            'method': method_value
        }
        response = requests.request(method_value, url, data=method_data)
        print(f'{method_value} / {method_data["method"]} - {response.text}')

def loop_with_correct_and_uncorrect_data(url, list_methods):
    print('Запускаем цикл по сценарию когда тип метода совпадает и не совпадает с переданными данными в параметрах method:')
    for method_value in list_methods:
        for method_params in list_methods:
            method_data = {
            'method': method_params
        }
            if method_value == 'GET':
                response = requests.request(method_value, url, params=method_data)
            else:
                response = requests.request(method_value, url, data=method_data)
            print(f'{method_value} / {method_data["method"]} - {response.text}')
        print()


requests_whithout_any_params(link, list_with_methods)
print()
requests_out_of_lists(link, methods_out_of_list)
print()
loop_with_correct_and_uncorrect_data(link, list_with_methods)

