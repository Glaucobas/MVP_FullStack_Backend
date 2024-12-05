from flask import Flask #, request, send_from_directory, render_template
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS

from model import Session
from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
from schemas.tabelas import *
from schemas.error import *
from schemas.funcoes import *

# from logger import logger
import logging

# Cria um logger
logger = logging.getLogger(__name__) 
logger.setLevel(logging.DEBUG)

# Cria um handler para o console 
console_handler = logging.StreamHandler() 
console_handler.setLevel(logging.DEBUG)

# Cria um handler para um arquivo 
file_handler = logging.FileHandler('./log/app.log') 
file_handler.setLevel(logging.WARNING) 

# Define um formatador 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
console_handler.setFormatter(formatter) 
file_handler.setFormatter(formatter) 

# Adiciona os handlers ao logger 
logger.addHandler(console_handler) 
logger.addHandler(file_handler)

info = Info(title = "Controle Financeiro", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#define tags
documentacao_tag = Tag(name="Documentação", description="Seleção de documentação: Swager")
home_tag         = Tag(name="Inicial",      description="Página Inicial")
categoria_tag    = Tag(name="Categoria",    description="Adição, visualização e remoção de categorias da base")
banco_tag        = Tag(name="Banco",        description="Adição, visualização e remoção de Instiuições Financeiras da base")
agencia_tag      = Tag(name="Agência",      description="Adição, visualização e remoção de Agências Bancárias da base")

# Metodos GET -----------------------------------------------------------------------------

# Consulta a Documentação 
@app.get('/', tags=[documentacao_tag])
def documentacao():
    """ Redireciona para /openapi, tela que permite a escolha do estilo de documentação. """

    return redirect('/openapi')

# Tela inicial do sistema: exibe uma lista das categorias cadastradas
@app.get('/index', tags=[home_tag], 
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def home():
    """ Tela inicial """
    
    # Busca as categorias cadastradas e as exibe na tabela
    logger.debug(f"Coletando categorias")
    
    # criando conexão com a base
    session = Session()
    
    try:
        # fazendo a busca
        categoria = session.query(Categorias).order_by(Categorias.debCred, Categorias.idCategoria).all()

        if not categoria:
            # se não há categorias cadastrados
            return {"categorias": []}, 200
        else: 
            logger.debug(f"%d categorias econtradas" % len(categoria))
            
            # retorna a representação de produto
            return listar_categorias(categoria), 200
    except Exception as e:
        logger.error(f"Erro ao consultar categoria #{categoria}: {str(e)}") 
        return {"message": "Erro interno do servidor"}, 500
    finally:
        session.close() # Fechar a sessão

# Consulta o cadastro de categorias
@app.get('/categoria', tags=[categoria_tag], 
         responses={"200": ListagemCategoriasSchema, "404": ErrorSchema})
def get_categoria():
    """ Faz a busca por todas as Categorias cadastradas 
        e retorna uma representação da listagem de categorias. """
    
    logger.debug(f"Coletando categorias")
    
    # criando conexão com a base
    session = Session()
    
    try:
        # fazendo a busca
        categoria = session.query(Categorias).order_by(Categorias.idCategoria).all()

        if not categoria:
            # se não há categorias cadastrados
            return {"categorias": []}, 200
        else: 
            logger.debug(f"%d categorias econtradas" % len(categoria))
            
            # retorna a representação de produto
            return listar_categorias(categoria), 200
    except Exception as e:
        logger.error(f"Erro ao consultar categoria #{categoria}: {str(e)}") 
        return {"message": "Erro interno do servidor"}, 500
    finally:
        session.close() # Fechar a sessão 

# Consulta o cadastro de bancos
@app.get('/banco', tags=[banco_tag], 
         responses={"200": ListagemBancosSchema, "404": ErrorSchema})
def get_banco():
    """ Faz a busca por todas as Instituições Financeiras cadastradas 
        e retorna uma representação da listagem de Instituições. """
    
    logger.debug(f"Coletando Instituições Financeiras")
    
    # criando conexão com a base
    session = Session()
    
    try:
        # fazendo a busca
        bancos = session.query(Bancos).order_by(Bancos.idBanco).all()

        if not bancos:
            # se não há Instituições Financeiras cadastradas
            return {"bancos": []}, 200
        else: 
            logger.debug(f"%d Instituições Financeiras econtradas" % len(bancos))
            
            # retorna a representação de produto
            return listar_bancos(bancos), 200
    except Exception as e:
        logger.error(f"Erro ao consultar Instituições Financeiras #{bancos}: {str(e)}") 
        return {"message": "Erro interno do servidor"}, 500
    finally:
        session.close() # Fechar a sessão 

# Consulta o cadastro de Agencias
@app.get('/agencia', tags=[agencia_tag], 
         responses={"200": ListagemAgenciasSchema, "404": ErrorSchema})
def get_agencia():
    """ Faz a busca por todas as agências bancárias cadastradas 
        e retorna uma representação da listagem de Instituições. """
    
    logger.debug(f"Coletando Agencias Bancárias")
    
    # criando conexão com a base
    session = Session()
    
    try:
        # fazendo a busca
        agencias = session.query(Agencias).order_by(Agencias.idBanco, Agencias.idAgencia).all()

        if not agencias:
            # se não há Instituições Financeiras cadastradas
            return {"agencias": []}, 200
        else: 
            logger.debug(f"%d Agências bancárias econtradas" % len(agencias))
            
            # retorna a representação de produto
            return listar_agencias(agencias), 200
    except Exception as e:
        logger.error(f"Erro ao consultar Instituições Financeiras #{agencias}: {str(e)}") 
        return {"message": "Erro interno do servidor"}, 500
    finally:
        session.close() # Fechar a sessão 

# Metodos POST -----------------------------------------------------------------------------

# Grava no cadastro de categorias
@app.post('/categoria', tags=[categoria_tag], 
          responses={"200": CategoriasViewSchema, "409": ErrorSchema, "400":ErrorSchema})

def add_categoria(form: CategoriasSchema):
    """ Adiciona uma nova Categoria de despesas à base de dados 
        e retorna uma representação das categorias. """
    
    categoria = Categorias(
        idCategoria = form.idCategoria,
        debCred     = form.debCred)
    
    logger.debug(f"Adicionando nova Categoria: '{categoria.idCategoria}'")

    try:
        # criando conexão com a base
        session = Session()

        # adicionando produto
        session.add(categoria)

        # efetivando o comando de adição do novo produto ao item na tabela
        session.commit()

        logger.debug(f"Adicionada nova Categoria: '{categoria.idCategoria}'")
        return apresenta_categoria(categoria), 200
    
    except IntegrityError as e:
        session.rollback()
        
        # como a duplicidade de nome é a provável razão do IntegrityError
        erro_msg = "Categoria com o mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar nova categoria '{categoria.idCategoria}', {error_msg}")
        return {"message": error_msg }, 409
    
    except Exception as e:
        session.rollback()
        
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo item :/"
        logger.warning(f"Erro ao adicionar nova categoria '{categoria.idCategoria}', {str(e)}")
        return {"message": error_msg }, 400
    finally:
        session.close() # Fechar a sessão 

# Grava no cadastro de bancos
@app.post('/banco', tags=[banco_tag], 
          responses={"200": BancosViewSchema, "409": ErrorSchema, "400":ErrorSchema})

def add_banco(form: BancosSchema):
    """ Adiciona uma nova Instituição Financeira à base de dados 
        e retorna uma representação das Instituições. """
    
    banco = Bancos(
        idBanco   = form.idBanco,
        descricao = form.descricao)
    
    logger.debug(f"Adicionando novo banco: '{banco.idBanco}'")

    try:
        # criando conexão com a base
        session = Session()

        # adicionando produto
        session.add(banco)

        # efetivando o comando de adição do novo produto ao item na tabela
        session.commit()

        logger.debug(f"Adicionada novo  banco: '{banco.idBanco}'")
        return apresenta_banco(banco), 200
    
    except IntegrityError as e:
        session.rollback()
        
        # como a duplicidade de nome é a provável razão do IntegrityError
        erro_msg = "Instituição Financeira com o mesmo código já salvo na base :/"
        logger.warning(f"Erro ao adicionar nova Instiuição Financeira '{banco.idBanco}', {error_msg}")
        return {"message": error_msg }, 409
    
    except Exception as e:
        session.rollback()
        
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo item :/"
        logger.warning(f"Erro ao adicionar nova Instituição Financeira '{banco.idBanco}', {str(e)}")
        return {"message": error_msg }, 400
    finally:
        session.close() # Fechar a sessão 

# Grava no cadastro de Agencias
@app.post('/agencia', tags=[agencia_tag], 
          responses={"200": AgenciasViewSchema, "409": ErrorSchema, "400":ErrorSchema})

def add_agencia(form: AgenciasSchema):
    """ Adiciona uma nova agência banária à base de dados 
        e retorna uma representação das agências. """

    agencia = Agencias(
        idBanco   = form.idBanco,
        idAgencia = form.idAgencia,
        descricao = form.descricao)
    
    logger.debug(f"Adicionando nova Agencia Bancária:'{agencia.idBanco}','{agencia.idAgencia}','{agencia.descricao}'")
    
    try:
        # criando conexão com a base
        session = Session()

        # adicionando produto
        session.add(agencia)

        # efetivando o comando de adição do novo produto ao item na tabela
        session.commit()

        logger.debug(f"Adicionada nova Agência Bancária: '{agencia.idBanco}', '{agencia.idAgencia}'")
        return apresenta_agencia(agencia), 200
    
    except IntegrityError as e:
        session.rollback()
        
        # como a duplicidade de nome é a provável razão do IntegrityError
        erro_msg = "Agência com o mesmo código já salvo na base :/"
        logger.warning(f"Erro ao adicionar nova agência bancária '{agencia.idBanco}', '{agencia.idAgencia}', {error_msg}")
        return {"message": error_msg }, 409
    
    except Exception as e:
        session.rollback()
        
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar o novo item :/"
        logger.warning(f"Erro ao adicionar nova Instituição Financeira '{agencia.idBanco}', '{agencia.idAgencia}', {str(e)}")
        return {"message": error_msg }, 400
    finally:
        session.close() # Fechar a sessão 

# Metodos DELETE -----------------------------------------------------------------------------

# Apaga uma categoria cadastrada
@app.delete('/categoria', tags=[categoria_tag], 
            responses={"200": CategoriasDelSchema, "404": ErrorSchema})
def del_categoria(query: CategoriasBuscaSchema):
    """ Apaga um item de categoria da base de dados a partir do seu identificador """
    
    categoria_id = unquote(query.idCategoria)
    
    logger.debug(f"Apagando dados sobre a categoria #{categoria_id}")
    
    # criando conexão com a base
    session = Session()
    
    try: 

        # fazendo a remoção
        count = session.query(Categorias).filter(Categorias.idCategoria == categoria_id).delete()

        if count:
            session.commit()

            # Retorna uma mensagem confirmando a remoção do item
            logger.debug(f"Deletada categoria #{categoria_id}")
            return {"message": "Categoria removida", "id": categoria_id}
        else: 
            # se a categoria não foi encontrado
            error_msg = "Categoria não encontrado na base :/"
            logger.warning(f"Erro ao deletar categoria #'{categoria_id}', {error_msg}")
            return {"message": error_msg}, 404 
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao deletar categoria #{categoria_id}: {str(e)}") 
        return {"message": "Erro interno do servidor"}, 500
    finally:
       session.close() # Fechar a sessão 

# Apaga um banco cadastrado
@app.delete('/banco', tags=[banco_tag], 
            responses={"200": BancosDelSchema, "404": ErrorSchema})

def del_banco(query: BancosBuscaSchema):
    """ Apaga uma Instiuição Financeira da base de dados a partir do seu identificador """
    
    if query.idBanco is not None:
        try:
            banco_id = int(query.idBanco)
        except ValueError:
            logger.error(f"idBanco deve ser um número inteiro válido") 
            banco_id = None   
    else:
        banco_id = None
    
    logger.debug(f"Apagando dados sobre a Instituição Financeira #{banco_id}")
    
    # criando conexão com a base
    session = Session()
    
    try: 

        # fazendo a remoção
        count = session.query(Bancos).filter(Bancos.idBanco == banco_id).delete()

        if count:
            session.commit()

            # Retorna uma mensagem confirmando a remoção do item
            logger.debug(f"Deletada Instituição Financeira #{banco_id}")
            return {"message": "Instituição Financeira removida", "id": banco_id}
        else: 
            # se a categoria não foi encontrado
            error_msg = "Instituição Financeira não encontrado na base :/"
            logger.warning(f"Erro ao deletar Instituição Financeira #'{banco_id}', {error_msg}")
            return {"message": error_msg}, 404 
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao deletar Instiuição Finaneira #{banco_id}: {str(e)}") 
        return {"message": "Erro interno do servidor"}, 500
    finally:
       session.close() # Fechar a sessão 

# Apaga uma agência bancária
@app.delete('/agencia', tags=[agencia_tag], 
            responses={"200": AgenciasDelSchema, "404": ErrorSchema})

def del_agencia(query: AgenciasBuscaSchema):
    """ Apaga uma Agência Bancária da base de dados a partir do seu identificador """
    
    if query.idBanco is not None and query.idAgencia is not None:
        try:
            banco_id = int(query.idBanco)
            agencia_id = int(query.idAgencia)
        except ValueError:
            logger.error(f"código do banco e/ou agencia deve ser um número inteiro válido") 
            banco_id = None   
            agencia_id = None
    else:
        banco_id = None
        agencia_id = None

    logger.debug(f"Apagando Agência Bancária #{banco_id}, #{agencia_id}")
    
    # criando conexão com a base
    session = Session()
    
    try: 

        # fazendo a remoção
        count = session.query(Agencias).filter(Agencias.idBanco == banco_id, 
                                               Agencias.idAgencia == agencia_id).delete()

        if count:
            session.commit()

            # Retorna uma mensagem confirmando a remoção do item
            logger.debug(f"Deletada Agência Bancária #{banco_id, agencia_id}")
            return {"message": "Agência Bancária removida", "id": (banco_id, agencia_id)}
        else: 
            # se a categoria não foi encontrado
            error_msg = "Agência Bancária não encontrado na base :/"
            logger.warning(f"Erro ao deletar Agência Bancária #'{banco_id, agencia_id}', {error_msg}")
            return {"message": error_msg}, 404 
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao deletar Agência Bancária #{banco_id, agencia_id}: {str(e)}") 
        return {"message": "Erro interno do servidor"}, 500
    finally:
       session.close() # Fechar a sessão 