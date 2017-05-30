import json
import requests

gc_json = {'email':'kitongajoseph@gmail.com', 'event_name':'Joe Kitonga Roast'}
ct_json = {'confirmation_num':'8945450aea'}

def test_route(r, json_obj):  
    try:
        base_url = "http://localhost:8000/api/{}/"
        return_val = requests.post(base_url.format(r), json=json_obj)
        if r == 'generate_confirmation':
            ct_json['confirmation_num'] = return_val.json()['confirmation_num']
        print(json.dumps(return_val.json(), indent=4))
    except:
        print('fuck')
    

if __name__ == '__main__':
    while(True): 
        print('1. generate_confirmation')
        print('2. confirm_ticket')
        route = input('Choose: ')
        if route == '1':
            test_route('generate_confirmation', gc_json)
        else:
            test_route('confirm_ticket', ct_json)