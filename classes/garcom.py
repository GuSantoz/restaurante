from .funcionario import Funcionario
from .mesa import Mesa
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Garcom(Funcionario):
    __tablename__ = "garcons"
    id = Column(Integer, ForeignKey("funcionarios.id"), primary_key=True)
    bonus = Column(Integer, default=0)

    __mapper_args__ = {
        "polymorphic_identity": "Garcom",
    }

    mesas = relationship("Mesa", back_populates="garcom")

    def __init__(self, nome, turno, salario, bonus = 0):
        super().__init__(nome, turno, salario)
        self.bonus = bonus

    def fechar_conta(self, vlr_pago, gorjeta, mesa):
        if vlr_pago < mesa.conta and vlr_pago > 0:
            print(f'Valor insuficiente, ainda faltam {mesa.conta - vlr_pago:.2f} R$')

        elif vlr_pago < 0:
            print('O valor nao pode ser negativo!')

        elif vlr_pago > mesa.conta:
            print(f'TROCO: {vlr_pago - mesa.conta}')
            self.remover_mesa(mesa)
            mesa.status = False
            if gorjeta:
                mesa.gorjeta = True
                self.bonus += mesa.calcular_gorjeta()
        else:
            self.remover_mesa(mesa)
            mesa.status = False
            if gorjeta:
                mesa.gorjeta = True
                self.bonus += mesa.calcular_gorjeta()

    def remover_mesa(self, mesa):
        for i in self.mesas:
            if i.num == mesa.num:
                self.mesas.remove(i)

    def calcular_salario(self):
        return self.get_salario() + self.bonus
        
