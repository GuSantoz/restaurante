from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String, Float
from createdb import Base

class Funcionario(Base, ABC):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    turno = Column(String)
    __salario = Column(Float)

    cargo = Column(String)
    __mapper_args__ = {
        "polymorphic_identity": "funcionario",
        "polymorphic_on": cargo
    }

    def __init__(self, nome, turno, salario):
        self.nome = nome
        self.turno = turno
        self.__salario = salario

    @property
    def salario(self):
        return self.__salario
    
    @salario.setter
    def salario(self, salario):
        self.__salario = salario
    def get_salario(self):
        return self.__salario

    @abstractmethod
    def calcular_salario(self):
        pass