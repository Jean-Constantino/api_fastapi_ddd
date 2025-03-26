from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from infrastructure.database import database
from interface.api.users import router as users_router
#from models.user import User  # Importando o modelo de usuário

# Criar a aplicação FastAPI
app = FastAPI(
    title="FastAPI DDD with SQLModel",
    description="API seguindo Domain-Driven Design com SQLModel",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Configurar os routers
app.include_router(users_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    """Evento executado ao iniciar a aplicação"""
    SQLModel.metadata.create_all(database.engine)

@app.on_event("shutdown")
def on_shutdown():
    """Evento executado ao encerrar a aplicação"""
    pass

# Health Check Endpoint
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}

# Dependência para obter a sessão do banco de dados
def get_session():
    with Session(database.engine) as session:
        yield session

# Endpoint GET para listar todos os usuários
@app.get("/api/v1/users", tags=["users"])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

# Endpoint GET para obter um usuário por ID
@app.get("/api/v1/users/{id}", tags=["users"])
def get_user_by_id(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# Função para iniciar o servidor
def start_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)

if __name__ == "__main__":
    start_server()
