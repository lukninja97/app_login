import requests

base_url = "http://127.0.0.1:5002"

def post_login(email, senha):
    try:
        url = f"{base_url}/login"
        dados = {
            "email": str(email),
            "senha": str(senha)
        }

        resposta = requests.post(url, json=dados)

        return resposta.json()
    except Exception as e:
        return {
            "msg": "erro de login",
            "error": str(e)
        }

def get_usuarios(token):
    try:
        url = f"{base_url}/usuarios"
        resposta = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        return resposta.json()["usuarios"]
    except Exception as e:
        return {
            "msg": "erro de usuarios",
            "error": str(e)
        }

def post_usuarios(nome, email, senha, papel, token):
    try:
        url = f"{base_url}/usuarios"
        dados = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "papel": papel
        }
        resposta = requests.post(url, json=dados, headers={"Authorization": f"Bearer {token}"})
        print(resposta.json())
        return resposta.status_code
    except Exception as e:
        return {
            "msg": "erro de usuarios",
            "error": str(e)
        }