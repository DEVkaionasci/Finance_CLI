from dataclasses import dataclass, field
import datetime

@dataclass
class Transacao:
    tipo: str
    valor: float
    data_horario: datetime.datetime = field(
        default_factory=datetime.datetime.now,
        init=False
        ) 

    def __str__(self):
        return f'{self.data_horario:%d/%m/%Y %H:%M:%S}: {self.tipo}\nR${self.valor:.2f}'
