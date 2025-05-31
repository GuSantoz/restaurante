# from .funcionario import Funcionario
from .funcionario import Funcionario
from sqlalchemy import Column, Integer, ForeignKey, String

class Cozinheiro(Funcionario):
    __tablename__ = "cozinheiros"
    id = Column(Integer, ForeignKey("funcionarios.id"), primary_key=True)
    especialidade = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "Cozinheiro",
    }

    def __init__(self, nome, turno, salario, especialidade):
        super().__init__(nome, turno, salario)
        self.especialidade = especialidade

    def calcular_salario(self):
        return self.__salario
