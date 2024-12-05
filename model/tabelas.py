from sqlalchemy import Column, ForeignKey, String, Integer, Float, Date
from sqlalchemy.orm import relationship, declarative_base

from datetime import date

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()

# Cadastro de Bancos
class Bancos(Base):
    __tablename__ = 'banco'

    idBanco   = Column(Integer,    primary_key=True)
    descricao = Column(String(40), nullable=False)
    
    agencia   = relationship("Agencias", back_populates="banco")

    def __init__(self, idBanco:int, descricao:str):
        """
        Cria a tabela de bancos

        Arguments:
            idBanco: Numero do banco junto ao banco central.
            descricao: Descrição que identifica o banco.
        """
        self.idBanco   = idBanco
        self.descricao = descricao

# Cadastro de Agencias Bancárias
class Agencias(Base):
    __tablename__ = 'agencia'

    idBanco   = Column(Integer,    ForeignKey('banco.idBanco'), primary_key=True)
    idAgencia = Column(Integer,    primary_key=True)
    descricao = Column(String(40), nullable=False)
    
    banco     = relationship("Bancos",     back_populates="agencia")
    conta     = relationship("Contas",     back_populates="agencia")
    transacao = relationship("Transacoes", back_populates="agencia")

    def __init__(self, idBanco:int, idAgencia:int, descricao:str):
        """
        Cria a tabela de Agencias Bancárias

        Arguments:
            idAgencia: Código da agencia bancária sem o dígito
            idBanco: Numero do banco junto ao banco central.
            descricao: Descrição que identifica o banco.
        """
        self.idBanco   = idBanco
        self.idAgencia = idAgencia
        self.descricao = descricao

class Contas(Base):
    __tablename__ = 'conta'

    idConta   = Column(Integer, primary_key=True)
    idAgencia = Column(Integer, ForeignKey('agencia.idAgencia'), primary_key=True)
    idRecurso = Column(Integer, ForeignKey('recurso.idRecurso'), primary_key=True)

    agencia   = relationship("Agencias",   back_populates="conta")
    transacao = relationship("Transacoes", back_populates="conta")
    recurso   = relationship("Recursos",   back_populates="conta")

    def __init__(self, idConta:int, idAgencia:int, idRecurso:int):
        """
        Cria a tabela de contas

        Arguments:
            idConta: Códgio da conta onde serão laçados os valores
            idAgencia: Identificação da agencia bancária
            idRecurso: Tipo de recurso da conta bancária (Cartão, Conta corrente, Poupança)
        """
        self.idConta   = idConta
        self.idAgencia = idAgencia
        self.idRecurso = idRecurso

# Cadastro de recursos (Cartões, Conta Poupança, Conta Corrente)
class Recursos(Base):
    __tablename__ = 'recurso'

    idRecurso = Column(Integer,    primary_key=True)
    descricao = Column(String(40), nullable=False)
    ativo     = Column(String(1),  nullable=False)
    
    conta     = relationship("Contas",     back_populates="recurso")
    transacao = relationship("Transacoes", back_populates="recurso")

    def __init__(self, idRecurso:int, descricao:str, ativo:str):
        """
        Cria a tabela de Recursos

        Arguments:
            idTipoConta: Tipo de conta bancária para o lançamento (Cartão, Conta corrente, Poupança)
            descricao: Descrição do tipo de conta
            ativo: Informa se a conta esta ativa ou inativa.
        """
        self.idRecurso = idRecurso
        self.descricao = descricao
        self.ativo     = ativo    

# Cadatro de tipos de Categoria de despesas 
class Categorias(Base):
    __tablename__ = 'categoria'

    idCategoria = Column(String(40), primary_key=True)
    debCred     = Column(String(1),  nullable=False)
    
    transacao = relationship("Transacoes", back_populates="categoria")

    def __init__(self, idCategoria:str, debCred:str):
        """
        Cria a tabela de categoria

        Arguments:
            idCategoria: Código da categoria de lançamento
            debCred: Informa se a conta é um débito ou crédito
        """
        self.idCategoria = idCategoria
        self.debCred     = debCred

# Lançamentos de valores 
class Transacoes(Base):
    __tablename__ = 'transacao'

    data        = Column(Date,        default=date.today,                  primary_key=True)
    idCategoria = Column(String(40),  ForeignKey('categoria.idCategoria'), primary_key=True)
    idConta     = Column(Integer,     ForeignKey('conta.idConta'),         primary_key=True)
    idAgencia   = Column(Integer,     ForeignKey('agencia.idAgencia'),     primary_key=True)
    idRecurso   = Column(Integer,     ForeignKey('recurso.idRecurso'),     primary_key=True)
    lancamento  = Column(String(200), nullable=False)
    valor       = Column(Float,       nullable=False)

    agencia     = relationship("Agencias",   back_populates="transacao")
    conta       = relationship("Contas",     back_populates="transacao")
    categoria   = relationship("Categorias", back_populates="transacao")
    recurso     = relationship("Recursos",   back_populates="transacao")

    def __init__(self, data:date, idCategoria:str, idConta:int, idAgencia:int, idRecurso:int, lancamento:str, valor:float):
        """
        Cria a tabela de transacao

        Arguments:
            data: data da transação
            idCategoria: Categoria do lançamento
            idConta: Identificação da conta de lançamento
            idAgencia: Identificação da agendia bancária
            idRecurso: Identificação do tipo de recurso da conta (Cartão, Poupança, Conta corrente)
            lancamento: Descrição do lançamento
            valor: valor do laçamento
        """
        self.data         = data
        self.idCategoria  = idCategoria
        self.idConta      = idConta
        self.idAgencia    = idAgencia
        self.idRecurso    = idRecurso
        self.lancamento   = lancamento
        self.valor        = valor 