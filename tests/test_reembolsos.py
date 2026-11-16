from datetime import date, timedelta
from fastapi import status
from src.models.usuario import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_criar_reembolso_sem_autenticacao(client):
    response = client.post(
        "/reembolsos/",
        json={
            "categoria": "Transporte",
            "valor": 100.0,
            "data_despesa": str(date.today()),
            "justificativa": "Viagem de táxi",
            "referencia_comprovante": "COMP-001"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_login_sucesso_e_falha(client, db_session):
    hashed_password = pwd_context.hash("senha123")
    utilizador = Usuario(
        nome="Utilizador Teste",
        email="teste@nexuscorp.com",
        senha_hash=hashed_password,
        perfil="Colaborador",
        departamento_id=1
    )
    db_session.add(utilizador)
    db_session.commit()

    response_sucesso = client.post(
        "/auth/login",
        data={"username": "teste@nexuscorp.com", "password": "senha123"}
    )
    assert response_sucesso.status_code == status.HTTP_200_OK
    dados = response_sucesso.json()
    assert "access_token" in dados
    assert dados["token_type"] == "bearer"

    response_falha = client.post(
        "/auth/login",
        data={"username": "teste@nexuscorp.com", "password": "errada"}
    )
    assert response_falha.status_code == status.HTTP_401_UNAUTHORIZED

def test_criar_reembolso_valor_invalido(client, db_session):
    hashed_password = pwd_context.hash("senha123")
    utilizador = Usuario(
        nome="Colab 2",
        email="colab2@nexuscorp.com",
        senha_hash=hashed_password,
        perfil="Colaborador",
        departamento_id=1
    )
    db_session.add(utilizador)
    db_session.commit()

    token_resp = client.post("/auth/login", data={"username": "colab2@nexuscorp.com", "password": "senha123"})
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/reembolsos/",
        headers=headers,
        json={
            "categoria": "Alimentação",
            "valor": 0.0,
            "data_despesa": str(date.today()),
            "justificativa": "Almoço",
            "referencia_comprovante": "COMP-999"
        }
    )
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]

def test_criar_reembolso_data_futura(client, db_session):
    hashed_password = pwd_context.hash("senha123")
    utilizador = Usuario(
        nome="Colab 3",
        email="colab3@nexuscorp.com",
        senha_hash=hashed_password,
        perfil="Colaborador",
        departamento_id=1
    )
    db_session.add(utilizador)
    db_session.commit()

    token_resp = client.post("/auth/login", data={"username": "colab3@nexuscorp.com", "password": "senha123"})
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data_futura = date.today() + timedelta(days=3)
    response = client.post(
        "/reembolsos/",
        headers=headers,
        json={
            "categoria": "Material",
            "valor": 50.0,
            "data_despesa": str(data_futura),
            "justificativa": "Compra futura",
            "referencia_comprovante": "COMP-888"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_criar_reembolso_duplicado_rn05(client, db_session):
    hashed_password = pwd_context.hash("senha123")
    utilizador = Usuario(
        nome="Colab Dup",
        email="colabdup@nexuscorp.com",
        senha_hash=hashed_password,
        perfil="Colaborador",
        departamento_id=1
    )
    db_session.add(utilizador)
    db_session.commit()

    token_resp = client.post("/auth/login", data={"username": "colabdup@nexuscorp.com", "password": "senha123"})
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "categoria": "Transporte",
        "valor": 75.0,
        "data_despesa": str(date.today()),
        "justificativa": "Uber",
        "referencia_comprovante": "DUP-COMP-01"
    }

    resp1 = client.post("/reembolsos/", headers=headers, json=payload)
    assert resp1.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]

    resp2 = client.post("/reembolsos/", headers=headers, json=payload)
    assert resp2.status_code == status.HTTP_400_BAD_REQUEST

def test_autoaprovacao_reembolso_rn09(client, db_session):
    hashed_password = pwd_context.hash("senha123")
    utilizador = Usuario(
        nome="Gestor Dono",
        email="gestordon@nexuscorp.com",
        senha_hash=hashed_password,
        perfil="Gestor",
        departamento_id=1
    )
    db_session.add(utilizador)
    db_session.commit()

    token_resp = client.post("/auth/login", data={"username": "gestordon@nexuscorp.com", "password": "senha123"})
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp_criacao = client.post(
        "/reembolsos/",
        headers=headers,
        json={
            "categoria": "Alimentação",
            "valor": 120.0,
            "data_despesa": str(date.today()),
            "justificativa": "Jantar de equipa",
            "referencia_comprovante": "AUTO-01"
        }
    )
    
    if resp_criacao.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
        solicitacao_id = resp_criacao.json().get("id")
        
        resp_analise = client.post(
            f"/reembolsos/{solicitacao_id}/analisar",
            headers=headers,
            json={"decisao": "Aprovado", "observacao": "Auto-aprovação"}
        )
        assert resp_analise.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST]