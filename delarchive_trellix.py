import argparse
import requests

def get_acess_token(client_id, secret):
    url = "https://auth.trellix.com/auth/realms/IAM/protocol/openid-connect/token"
    auth = (client_id, secret)
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "scope": "xdr.alr.r xdr.alr.rw xdr.dbr.r xdr.dbr.rw xdr.dp.r xdr.dp.rw xdr.ind.r xdr.ind.rw xdr.org.adm xdr.rul.r xdr.rul.rw xdr.so.r xdr.so.rw xdr.srh.adv xdr.srh.r xdr.srh.rw",
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data, auth=auth)
    return response.json()['access_token']


def get_archive_saved(helix_id, access_token):
    url = f"https://xdr.trellix.com/helix/id/{helix_id}/api/v1/search/archive/?limit=100"
    headers = {
        "accept": "application/json",
        "x-trellix-api-token": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def del_all_archive_saved(helix_id, access_token):
    url = f"https://xdr.trellix.com/helix/id/{helix_id}/api/v1/search/archive/"
    headers = {
        "accept": "application/json",
        "x-trellix-api-token": f"Bearer {access_token}"
    }
    response = requests.delete(url, headers=headers)
    return response.status_code


def main():
    parser = argparse.ArgumentParser(description='Gerenciador de pesquisas Trellix')
    parser.add_argument('--helix', required=True, help='id do helix')
    parser.add_argument('--id', required=True, help='client id')
    parser.add_argument('--secret', required=True, help='secret')
    parser.add_argument('--action', choices=['listar', 'deletar'], required=True, 
                       help='Ação a ser executada: listar ou deletar pesquisas')

    args = parser.parse_args()
    
    access_token = get_acess_token(args.id, args.secret)

    if args.action == 'listar':
        data = get_archive_saved(args.helix, access_token)
        pesquisas = data['data']
        print("\nPesquisas salvas:")
        for pesquisa in pesquisas:
            print(f"ID: {pesquisa.get('id')} - Nome: {pesquisa.get('query')}")
    
    elif args.action == 'deletar':
        status = del_all_archive_saved(args.helix, access_token)
        if status == 204:
            print("\nTodas as pesquisas foram deletadas com sucesso!")
        else:
            print(f"\nErro ao deletar pesquisas. Status code: {status}")


if __name__ == "__main__":
    main()

# import os
# from dotenv import load_dotenv
# load_dotenv()

# client_id = os.getenv('client_id')
# secret = os.getenv('secret')
# access_token = get_acess_token(client_id,secret)
# helix_id = os.getenv('t_helix_id')
# data = get_archive_saved(helix_id, access_token)
# pesquisas = data['data']
# meta = data['meta']['totalCount']

# print(f"Existe {meta} cadastradas")
# count = 1
# for p in pesquisas:
#     print(f"{count} - {p['query']}")
#     count += 1