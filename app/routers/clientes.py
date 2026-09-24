from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session, select

from app.database import engine
from app.models import Cliente, ClienteCreate, ClienteUpdate, ClienteResponse

router = APIRouter(prefix='/clientes', tags=["Clientes"])

# EndsPoint METHOD + PATH, ex.: "GET /clientes/18"

# =====================================================================================
# Get /clientes/
# Lista todos os clientes cadastrados no sistema
# ======================================================================================
@router.get('/', 
            response_model=list[ClienteResponse],
            status_code=status.HTTP_200_OK,
            summary="Listar clientes cadastrados"
            )
def listar_clientes():
    # Abre uma sessão com o banco de dados
    with Session(engine) as session:

        # Monta uma consulta para buscar os clientes
        clientes = session.exec(select(Cliente)).all()

        # Retorna a lista de clientes encontrados
        return clientes

# ======================================================================================
# Get /clientes/{id}
# Busca um cliete específico pelo ID
# ======================================================================================
@router.get('/{cliente_id}', response_model=ClienteResponse, status_code=status.HTTP_200_OK, summary ="Obter cliente pelo ID")
def obter_cliente(id: int):
    # Abre uma sessão com o banco
    with Session(engine) as session:

        # Procura cliente pelo ID
        cliente = session.get(Cliente, id)

        # Se não encontrou, retorna HTTP 404
        if cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente de ID ={id} não encontrado"
            )

        # Retorna o cliente encontrado.
        return cliente

# ======================================================================================
# POST /clientes/
# Cadastrar um novo cliente
# ======================================================================================
@router.post('/',
             response_model=ClienteResponse,
             status_code= status.HTTP_201_CREATED,
             summary="Cadastrar novo cliente"
             )
def criar_cliente(cliente: ClienteCreate):
    # Abre uma sessão com o banco.
    with Session(engine) as session:

        # Cria o objeto Cliente usando os dados recebidos.
        novo_cliente = Cliente.model_validate(cliente)

        # Adiciona o cliente a sessão
        session.add(novo_cliente)

        # Salva as alterações no banco.
        session.commit()

        # Atualiza o objeto com o ID gerado pelo banco.
        session.refresh(novo_cliente)

        # Retorna o cliente criado.
        return novo_cliente

# ======================================================================================
# PUT /clientes/{id}
# Atualiza os dados de um cliente existente.
# ======================================================================================
@router.put('/{cliente_id}', response_model=ClienteResponse)
def atualizar_cliente(id: int, dados:ClienteUpdate):
    # Abre uma sessão com o banco
    with Session(engine) as session:

        # Procura o cliente pelo id
        cliente = session.get(Cliente, id)

        # Se não encontrou, retorna 404
        if cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"Cliente de ID={id} não foi encontrado"
            )

        #Obtém somente os campos enviados na requisição.
        dados_atualizados = dados.model_dump(exclude_unset=True)

        # Atualiza os campos do cliente
        cliente.sqlmodel_update(dados_atualizados)

        # Salva as alterações no banco
        session.add(cliente)
        session.commit()

        # Atualiza o objeto com os dados atuais do banco.
        session.refresh(cliente)

        # Retorna o cliente atualizado.
        return cliente

# ======================================================================================
# DELETE /clientes/{id}
# Exclui um cliente existente.
# ======================================================================================

@router.delete('/{cliente_id}', status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(id: int):
    # Abre uma sessão com o banco
    with Session(engine) as session:

        # Procura o cliente pelo ID
        cliente = session.get(Cliente, id)

        # Se não encontrou, retorna 404
        if cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente de ID={id} não foi encontrado."
            )

        # Remove o cliente da sessão
        session.delete(cliente)

        # Salva a esclusão no banco
        session.commit()
