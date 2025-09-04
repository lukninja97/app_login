import requests

base_url = "http://10.135.233.6:5002"

def post_login(email, senha):
    try:
        url = f"{base_url}/login"
        dados = {
            "email": email,
            "senha": senha,
        }
        response = requests.post(url, json=dados)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }

def get_usuarios(token):
    try:
        url = f"{base_url}/usuarios"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }

def post_usuario(nome, email, senha, papel, token):
    try:
        url = f"{base_url}/usuarios"
        dados = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "papel": papel,
        }
        response = requests.post(url, json=dados, headers={"Authorization": f"Bearer {token}"})
        return response.status_code
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }