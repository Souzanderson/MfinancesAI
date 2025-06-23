from fastapi import FastAPI
from pydantic import BaseModel
from src.chat.chat import classificar_transacao
from src.repository.result import Item
app = FastAPI()

from pydantic import Field
from datetime import datetime
from typing import Optional, List, Any
from fastapi.middleware.cors import CORSMiddleware

from src.repository.user import User
from fastapi import HTTPException

from src.middlewares.bearer_middleware import BearerTokenAuth
from fastapi import Depends

auth_scheme = BearerTokenAuth(auto_error=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MensagemRequest(BaseModel):
    mensagem: str = Field(..., alias="message")
    
class ResultadoResponse(BaseModel):
    items: Optional[List[Any]] = None
    totais: Optional[Any] = None
    error: Optional[Any] = None
    
@app.post("/classificar", response_model=ResultadoResponse)
def classificar(
    mensagem_request: MensagemRequest,
    token: str = Depends(auth_scheme)
):
    try:
        # print(f"[INFO] token: {token}")
        user_id = User.id_user(token)
        resultado = classificar_transacao(mensagem_request.mensagem, user=token)
        if "error" in resultado:
            return {"items": [], "totais": None, "error": resultado["error"]}
        if "item" in resultado:
            item = Item.from_json(resultado, user_id)  # Valida e converte o resultado para Item
            response = item.distribuir_parcelas_e_inserir()  # Insere no banco de dados
            return {"items": response}
        
        if "produto" in resultado:
            # Converte o mês nominal para número
            meses = {
                "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
                "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
                "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12, 
                "atual": datetime.now().month
            }
            print(resultado)
            mes_num = meses.get(resultado["mes"].lower())
            if mes_num is None:
                mes_num = int(resultado["mes"])  # Se não for um mês nomeado, assume que é um número
            ano = datetime.now().year if resultado["ano"].lower() == "atual" else int(resultado["ano"])
            print(mes_num, ano)
            
            if "istotal" in resultado:
                item = Item.get_receitas_despesas_by_month_year(
                    month=mes_num,
                    year=ano, 
                    user_id=user_id
                )
                return {"totais": item}
            
            item = Item.get_by_month_year(
                month=mes_num,
                year=ano,
                user_id=user_id
            )

            return {"items": [item.dict() for item in item]}  # Retorna os itens encontrados
        
    except Exception as e:
        print(f"[ERROR] Error:  => ", e)
        return {"items": [], "totais": None, "error": "Erro ao processar a mensagem!"}

class LoginRequest(BaseModel):
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")

@app.post("/login")
def login(login_request: LoginRequest):
    response = User.login(**login_request.dict())
    if "error" in response:
        raise HTTPException(status_code=401, detail=response["error"])
    
    return response