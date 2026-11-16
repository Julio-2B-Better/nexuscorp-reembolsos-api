from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.solicitacao import SolicitacaoReembolso
from src.schemas.reembolso import SolicitacaoCriar, SolicitacaoResposta, AnaliseReembolsoSchema
from src.services.seguranca import obter_utilizador_atual
from src.models.usuario import Usuario

router = APIRouter(prefix="/reembolsos", tags=["Reembolsos"])

@router.post("/aprovar_financeiro")
def aprovar_reembolso(utilizador = Depends(obter_utilizador_atual)):
    if utilizador.get("perfil") != "Financeiro":
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas o Financeiro pode aprovar.")
    return {"mensagem": "Aprovado com sucesso"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SolicitacaoResposta)
def registar_solicitacao(
    dados: SolicitacaoCriar, 
    db: Session = Depends(get_db),
    utilizador = Depends(obter_utilizador_atual)
):
    if dados.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor da despesa deve ser maior que zero.")

    if dados.data_despesa > date.today():
        raise HTTPException(status_code=400, detail="Não são permitidas despesas com datas futuras.")

    user_id = int(utilizador["sub"])

    comprovante_duplicado = db.query(SolicitacaoReembolso).filter(
        SolicitacaoReembolso.referencia_comprovante == dados.referencia_comprovante,
        SolicitacaoReembolso.solicitante_id == user_id
    ).first()

    if comprovante_duplicado:
        raise HTTPException(status_code=400, detail="Já existe uma despesa registrada com este comprovante.")

    nova_solicitacao = SolicitacaoReembolso(
        solicitante_id=user_id,
        categoria=dados.categoria,
        valor=dados.valor,
        data=dados.data_despesa,
        justificativa=dados.justificativa,
        referencia_comprovante=dados.referencia_comprovante,
        situacao="Rascunho" 
    )
    
    db.add(nova_solicitacao)
    db.commit()
    db.refresh(nova_solicitacao)
    
    return nova_solicitacao

@router.post("/{solicitacao_id}/analisar", response_model=SolicitacaoResposta)
def analisar_solicitacao(
    solicitacao_id: int,
    analise: AnaliseReembolsoSchema,
    db: Session = Depends(get_db),
    utilizador = Depends(obter_utilizador_atual)
):
    solicitacao = db.query(SolicitacaoReembolso).filter(SolicitacaoReembolso.id == solicitacao_id).first()
    
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    if solicitacao.solicitante_id == int(utilizador["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Não é permitido aprovar ou recusar a sua própria solicitação de reembolso."
        )

    perfil_usuario = utilizador.get("perfil")
    
    if perfil_usuario == "Colaborador":
        raise HTTPException(status_code=403, detail="Colaboradores não têm permissão para analisar solicitações.")
    
    if perfil_usuario == "Gestor":
        if utilizador.get("departamento_id") != solicitacao.solicitante.departamento_id:
            raise HTTPException(status_code=403, detail="Gestor só pode analisar solicitações do seu próprio departamento.")
        
        solicitacao.situacao = "Aprovado pelo Gestor" if analise.decisao.lower() == "aprovado" else "Recusado"

    elif perfil_usuario == "Financeiro":
        solicitacao.situacao = "Pago" if analise.decisao.lower() == "aprovado" else "Recusado"

    db.commit()
    db.refresh(solicitacao)
    
    return solicitacao

@router.get("/", response_model=list[SolicitacaoResposta])
def listar_solicitacoes(
    db: Session = Depends(get_db),
    utilizador = Depends(obter_utilizador_atual)
):
    perfil = utilizador.get("perfil")
    user_id = int(utilizador["sub"])
    
    if perfil == "Colaborador":
        solicitacoes = db.query(SolicitacaoReembolso).filter(
            SolicitacaoReembolso.solicitante_id == user_id
        ).all()
        
    elif perfil == "Gestor":
        departamento_id = utilizador.get("departamento_id")
        
        solicitacoes = db.query(SolicitacaoReembolso).join(Usuario).filter(
            Usuario.departamento_id == departamento_id
        ).all()
        
    elif perfil == "Financeiro":
        solicitacoes = db.query(SolicitacaoReembolso).all()
        
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Perfil de utilizador não reconhecido ou sem permissões."
        )
        
    return solicitacoes