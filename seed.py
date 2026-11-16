from src.database import SessionLocal, Base, engine
from src.models.departamento import Departamento # Confirme se o nome do model está correto
from src.models.usuario import Usuario
from services.seguranca import gerar_hash_senha

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if not db.query(Departamento).first():
    dept_ti = Departamento(nome="Tecnologia")
    dept_comercial = Departamento(nome="Comercial")
    db.add_all([dept_ti, dept_comercial])
    db.commit()

    utilizadores = [
        Usuario(nome="Bruno (Colaborador TI)", email="bruno@nexus.com", senha_hash=gerar_hash_senha("123456"), perfil="Colaborador", departamento_id=1),
        Usuario(nome="Carlos (Gestor TI)", email="carlos@nexus.com", senha_hash=gerar_hash_senha("123456"), perfil="Gestor", departamento_id=1),
        Usuario(nome="Ana (Financeiro)", email="ana@nexus.com", senha_hash=gerar_hash_senha("123456"), perfil="Financeiro", departamento_id=2)
    ]
    db.add_all(utilizadores)
    db.commit()
    print("Base de dados populada com sucesso!")

db.close()