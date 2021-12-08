import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
parsing_json_text = json.loads(json_text)
dict_key = 'messages'
second_dict_key = 'message'
list_with_dictions = parsing_json_text[dict_key]
second_obj_of_list = list_with_dictions[1]
message_of_second_dict = second_obj_of_list[second_dict_key]
print(message_of_second_dict)
