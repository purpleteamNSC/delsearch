import requests
import os


# banner del search
def print_banner():
    os.system('cls') if os.name == 'nt' else os.system('clear')
    
    banner = r"""
     ____       _ ____                      _     
    |  _ \  ___| / ___|  ___  __ _ _ __ ___| |__  
    | | | |/ _ \ \___ \ / _ \/ _` | '__/ __| '_ \ 
    | |_| |  __/ |___) |  __/ (_| | | | (__| | | |
    |____/ \___|_|____/ \___|\__,_|_|  \___|_| |_|                                     
    """
    print("\033[91m" + banner + "\033[0m")

    print('')


# recuperar searches
def get_saved_searches(helix_id, api_key):
    
    url = f"https://apps.fireeye.com/helix/id/{helix_id}/api/v3/search/saved/?limit=100"
    headers = {"accept": "application/json", "x-fireeye-api-key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        return "Error: " + str(e)


# deleta uma search
def delete_saved_searche_by_id(helix_id, api_key, id):
    url = f"https://apps.fireeye.com/helix/id/{helix_id}/api/v3/search/saved/{id}"
    headers = {"accept": "application/json", "x-fireeye-api-key": api_key}

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            print(f"\033[91mSearch com ID {id} deletado com sucesso.\033[0m")
        return response.status_code
    except requests.exceptions.RequestException as e:
        return "Error: " + str(e)


# funçoes extras

# inputs
def get_inputs(helix_id=None, api_key=None):
    
    while helix_id is None or len(helix_id) < 5:
        print_banner()
        helix_id = input("Insira ID do Helix lado Fireeye: ")
        if len(helix_id) < 5:
            continue

    
    while api_key is None or len(api_key) < 5:
        print_banner()
        api_key = input("Insira API key do Helix lado Fireeye: ")
        if len(api_key) < 5:
            continue

    return helix_id, api_key


# imprime as searches
def all_results(data):
    print("CODIGO - NOME - QUERY")
    print("")

    for result in data:
        print(f"{result['id']} - {result['name']}")
        print(f"{result['query']}")
        print("")


# EXECUCAO
try:
    helix_id, api_key = get_inputs()

    while True:
        print_banner()
        all_results(get_saved_searches(helix_id, api_key))
        id_del = input("Insira ID do saved search que deseja deletar ou 0 para sair: ")

        if id_del == "0":
            os.system('cls') if os.name == 'nt' else os.system('clear')
            print("Saindo do script delsearch_v2.")
            break
        else:
            delete_saved_searche_by_id(helix_id, api_key, id_del)
            input("Pressione Enter para continuar...")    
except KeyboardInterrupt:
    os.system('cls') if os.name == 'nt' else os.system('clear')
    print("\nSaindo do script delsearch_v2.")
    exit()
