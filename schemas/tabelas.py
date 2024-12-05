from pydantic import BaseModel
from typing import List

# Schemas -------------------------------------------------------------------------------------
class CategoriasSchema(BaseModel):
    """ Define como uma nova Categoria a ser inserida deve ser representada """

    idCategoria: str
    debCred: str

class BancosSchema(BaseModel):
    """ Define como uma nova Instituição Financeira a ser inserido deve ser representado """

    idBanco: int
    descricao: str

class AgenciasSchema(BaseModel):
    """ Define como uma nova Agância Bancária a ser inserida deve ser representado """

    idBanco: int
    idAgencia: int
    descricao: str


# Views Schemas -------------------------------------------------------------------------------
class CategoriasViewSchema(BaseModel):
    """ Define como uma nova Categoria deve ser representada """

    idCategoria: str
    debCred: str

class BancosViewSchema(BaseModel):
    """ Define como uma nova Instituição Financeira deve ser representada """

    idBanco: int
    descricao: str

class AgenciasViewSchema(BaseModel):
    """ Define como uma nova Agência Bancária bdeve ser representada """

    idBanco: int
    idAgencia: int
    descricao: str


# Listagens Schema ----------------------------------------------------------------------------
class ListagemCategoriasSchema(BaseModel):
    """ Define como uma listagem de Categorias será retornada. """

    categorias:List[CategoriasViewSchema]

class ListagemBancosSchema(BaseModel):
    """ Define como uma listagem de Instituições Financeiras será retornada. """

    bancos:List[BancosViewSchema]

class ListagemAgenciasSchema(BaseModel):
    """ Define como uma listagem de Agências Bancárias será retornada. """

    agencias:List[AgenciasViewSchema]


# Del Schemas ---------------------------------------------------------------------------------
class CategoriasDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    
    message: str
    idCategoria: str

class BancosDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    
    message: str
    idBanco: int

class AgenciasDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção. """
    
    message: str
    idBanco: int
    idAgencia: int


# Busca Schemas -------------------------------------------------------------------------------
class CategoriasBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca que será feita apenas com 
    base no nome da Categoria. """

    idCategoria: str

class BancosBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca que será feita apenas com 
    base no código da Instituição Financeira. """

    idBanco: int

class AgenciasBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca que será feita com 
    base no código da Instituição Financeiras e na Agência Bancária. """

    idBanco: int
    idAgencia: int
