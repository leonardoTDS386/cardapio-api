from datetime import date
from sqlmodel import SQLModel, Field

# =====================================================================
# CONCEITO DIDÁTICO: SQLModel (União entre Pydantic e SQLAlchemy)
# 1. Classes que herdam de SQLModel são Schemas Pydantic por padrão (validação).
# 2. Ao adicionar table=True, a classe também se torna uma Tabela no Banco de Dados.
#
# CONCEITO: Evolução de Esquema de Banco
# Ao adicionar um novo campo (como tempo_preparo_minutos) num modelo existente,
# o banco de dados precisa de uma migração (via Alembic) para rodar o
# comando SQL: ALTER TABLE itens_cardapio ADD COLUMN tempo_preparo_minutos INTEGER;
# =====================================================================


class ItemCardapioBase(SQLModel):
    """Campos comuns compartilhados tanto pelo Banco quanto pela API."""
    nome: str = Field(
        min_length=2, 
        max_length=100, 
        description="Nome do prato ou bebida"
    )
    descricao: str | None = Field(
        default=None, 
        max_length=255, 
        description="Descrição dos ingredientes ou detalhes do item"
    )
    preco: float = Field(
        gt=0, 
        description="Preço em reais (deve ser estritamente maior que zero)"
    )
    categoria: str = Field(
        default="Lanches", 
        description="Categoria do item: Lanches, Bebidas, Sobremesas, etc."
    )
    disponivel: bool = Field(
        default=True, 
        description="Indica se o item está disponível para pedido"
    )
    # Atributo adicionado na evolução de esquema via Migração Alembic:
    tempo_preparo_minutos: int | None = Field(
        default=None, 
        ge=1, 
        description="Tempo estimado de preparo em minutos (ex: 15, 30)"
    )


# =====================================================================
# CONCEITO: Modelo ORM (Tabela no PostgreSQL / SQLite)
# table=True avisa o SQLModel que esta classe mapeia a tabela itens_cardapio.
# =====================================================================
class ItemCardapio(ItemCardapioBase, table=True):
    __tablename__ = "itens_cardapio"

    id: int | None = Field(default=None, primary_key=True)


# =====================================================================
# CONCEITO: Schemas de Validação de Entrada e Saída (DTOs)
# - ItemCardapioCreate: o que o cliente envia no POST (sem id).
# - ItemCardapioUpdate: campos opcionais que podem ser atualizados no PUT/PATCH.
# - ItemCardapioResponse: o que a API devolve (garantindo id).
# =====================================================================
class ItemCardapioCreate(ItemCardapioBase):
    """Schema para validação do corpo da requisição no cadastro (POST)."""
    pass


class ItemCardapioUpdate(SQLModel):
    """Schema para atualização de dados (PUT/PATCH). Permite atualizar campos parciais."""
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = None
    categoria: str | None = None
    disponivel: bool | None = None
    tempo_preparo_minutos: int | None = None


class ItemCardapioResponse(ItemCardapioBase):
    """Schema retornado pela API nas consultas. Garante a presença do campo 'id'."""
    id: int


# Nova classe cliente base

class ClienteBase(SQLModel):
    """Campos comuns compartilhados pelo Banco e pela API"""
    nome: str = Field(
        min_length=2,
        max_length = 100,
        description="Nome do cliente"
    )
    cpf: str= Field(
        min_length=11,
        max_length = 11,
        description="CPF do cliente"
    )
    telefone: str = Field(
        max_length= 20,
        description="Telefone do cliente"
    )
    email: str = Field(
        max_length = 150,
        description="E-mail do cliente"
    )
    endereco: str = Field(
        max_length = 200,
        description="Endereço do cliente"
    )
    data_nascimento: date = Field(
        description="Data de nascimento do cliente"
    )

class Cliente(ClienteBase, table=True):
    __tablename__ = "clientes"

    id: int | None = Field(default=None, primary_key=True)

class ClienteCreate(ClienteBase):
    """Schema para validação dos dados de cadastro do cliente (POST)"""
    pass

class ClienteUpdate(SQLModel):
    """Schema para atualização dos dados do cliente (PUT/PATCH)."""
    nome: str | None = None # Opcional para caso queira alterar apenas um
    cpf: str | None = None
    telefone: str | None = None
    email: str | None = None
    endereco: str | None = None
    data_nascimento: date | None = None

class ClienteResponse(ClienteBase):
    """Schema retornado pela API nas consultas. Garante a presença do campo ID"""
    id: int