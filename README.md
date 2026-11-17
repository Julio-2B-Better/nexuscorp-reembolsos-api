# NexusCorp — API de Gestão de Reembolsos Corporativos

API REST desenvolvida em **Python (FastAPI)** para centralizar e automatizar o fluxo de reembolsos corporativos da **NexusCorp**, garantindo conformidade com rigorosas regras de negócio, controlo estrito de acessos por perfil e rastreabilidade total das decisões.

---

##  Autor
* **Aluno:** Júlio Cesar Bento da Silva Filho  
* **Contexto:** Projeto Acadêmico / Atividade 07 (NexusCorp)

---

##  Stack Tecnológica
* **Linguagem:** Python 3.10+
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **Base de Dados:** SQLite (com persistência relacional)
* **ORM:** SQLAlchemy
* **Validação de Dados:** Pydantic v2
* **Segurança e Autenticação:** Passlib (Bcrypt) & Python-Jose (JWT Bearer)
* **Testes Automatizados:** Pytest / TestClient

---

##  Perfis de Utilização e Responsabilidades
1. **Colaborador:** Regista, edita (em modo rascunho), envia e acompanha as suas próprias solicitações de reembolso.
2. **Gestor:** Analisa solicitações pertencentes exclusivamente aos colaboradores do seu departamento (aprova ou recusa).
3. **Financeiro:** Realiza a análise financeira final e regista a conclusão do pagamento.

---

##  Regras de Negócio Implementadas (Destaques)
* **RN01 & RN13 (Identificação e Credenciais):** Autenticação baseada em tokens JWT e hash seguro de passwords via bcrypt.
* **RN02 & RN03 (Confidencialidade e Departamento):** Isolamento restrito de dados, impedindo que colaboradores ou gestores acedam a informações de outros departamentos.
* **RN04, RN05 & RN06 (Integridade, Duplicidade e Período):** Bloqueio de valores negativos/zero, prevenção rigorosa de comprovantes duplicados e proibição de despesas com datas futuras.
* **RN07, RN08 & RN10 (Ciclo de Vida e Fluxo):** Imutabilidade de rascunhos após o envio, subordinação obrigatória ao aval do gestor antes do financeiro, e pagamentos restritos à aprovação financeira.
* **RN09 (Segregação de Responsabilidades):** Proibição absoluta de autoaprovação de solicitações.

---

##  Como Instalar e Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd nexuscorp-reembolsos-api
```

### 2. Criar e Ativar o Ambiente Virtual
* **No Windows (PowerShell):**
  ```bash
  python -m venv venv
  .\venv\Scripts\Activate
  ```
* **No Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação Localmente
```bash
uvicorn src.main:app --reload
```

### 5. Aceder à Documentação Interativa (Swagger UI)
Com a aplicação a correr, abra no seu navegador:
* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

---

##  Como Executar os Testes Automatizados
O projeto conta com uma suíte de testes robusta cobrindo a autenticação, segurança, validações e o ciclo de vida completo de aprovação.

Para executar os testes com o `pytest`, certifique-se de estar com o ambiente virtual ativado e execute:
```bash
pytest -v
```
*(Todos os testes estão configurados para rodar sobre uma base de dados isolada em memória).*
