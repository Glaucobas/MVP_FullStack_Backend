
from schemas.tabelas import *
from model.tabelas import Categorias, Bancos, Agencias

# Listas --------------------------------------------------------------------------------------
def listar_categorias(categorias: List[CategoriasSchema]):
    """ Retorna uma representação da categoria seguindo o schema definido em CategoriasViewSchema. """

    result = []
    for categoria in categorias:
        result.append({
            "idCategoria": categoria.idCategoria,
            "debCred":     categoria.debCred
        })
    return {"categorias": result}
 
def listar_bancos(bancos: List[BancosSchema]):
    """ Retorna uma representação da categoria seguindo o schema definido em CategoriasViewSchema. """

    result = []
    for banco in bancos:
        result.append({
            "idBanco":   banco.idBanco,
            "descricao": banco.descricao
        })
    return {"bancos": result}

def listar_agencias(agencias: List[AgenciasSchema]):
    """ Retorna uma representação da categoria seguindo o schema definido em CategoriasViewSchema. """

    result = []
    for agencia in agencias:
        result.append({
            "idBanco":   agencia.idBanco,
            "idAgencia": agencia.idAgencia,
            "descricao": agencia.descricao
        })
    return {"agencias": result}


# Apresenta -----------------------------------------------------------------------------------
def apresenta_categoria(categoria: Categorias):
    """ Retorna uma representação da categoria seguindo o schema definido em CategoriaViewSchema. """
    
    return {
        "idCategoria": categoria.idCategoria,
        "debCred":     categoria.debCred
    }

def apresenta_banco(banco: Bancos):
    """ Retorna uma representação da Instituição Financeira seguindo o schema definido em BancoViewSchema. """
    
    return {
        "idBanco":   banco.idBanco,
        "descricao": banco.descricao
    }

def apresenta_agencia(agencia: Agencias):
    """ Retorna uma representação da Instituição Financeira seguindo o schema definido em BancoViewSchema. """
    
    return {
        "idBanco":   agencia.idBanco,
        "idAgencia": agencia.idAgencia,
        "descricao": agencia.descricao
    }