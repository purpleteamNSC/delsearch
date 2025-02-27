import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_all_search_saved(helix_id, apikey):
    url = f"https://xdr.trellix.com/helix/id/{helix_id}/api/v3/search/saved/"
    headers = {
        "accept": "application/json",
        "x-fireeye-api-key": f"{apikey}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get('results',[])


def delete_search_saved(helix_id, apikey,id):
    url = f"https://xdr.trellix.com/helix/id/{helix_id}/api/v3/search/saved/{id}"
    headers = {
        "accept": "application/json",
        "x-fireeye-api-key": f"{apikey}"
    }
    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return f'Excluido o id: {id}'

    return f'error ao excluir o id: {id}'


h = os.getenv('f_helix_id')
a = os.getenv('fireeye_apikey')


consultas = get_all_search_saved(h,a)
for c in consultas:
    print(delete_search_saved(h,a,c['id']))
