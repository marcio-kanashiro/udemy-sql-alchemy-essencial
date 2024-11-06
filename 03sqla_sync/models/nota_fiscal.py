import sqlalchemy as sa
import sqlalchemy.orm as orm

from sqlalchemy.orm import Mapped

from datetime import datetime
from typing import List

from models.model_base import ModelBase
from models.revendedor import Revendedor
from models.lote import Lote

# Uma Nota Fiscal pode ter vários lotes
lotes_nota_fiscal = sa.Table(
    "lotes_nota_fiscal",
    ModelBase.metadata,
    sa.Column("id_nota_fiscal", sa.Integer, sa.ForeignKey("notas_fiscais.id")),
    sa.Column("id_lote", sa.Integer, sa.ForeignKey("lotes.id"))
)


class NotaFiscal(ModelBase):
    __tablename__: str = "notas_fiscais"

    id: int = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    data_criacao: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    valor: float = sa.Column(sa.DECIMAL(8,2), nullable=False)
    numero_serie: str = sa.Column(sa.String(45), unique=True, nullable=False)
    descricao: str = sa.Column(sa.String(200), nullable=False)

    id_revendedor: int = sa.Column(sa.Integer, sa.ForeignKey("revendedores.id"))
    revendedor: Mapped[Revendedor] = orm.relationship("Revendedor", lazy="joined")

    # Uma Nota Fiscal pode ter vários lotes e um Lote está ligado a uma nota fiscal
    lotes: Mapped[List[Lote]] = orm.relationship("Lote", secondary=lotes_nota_fiscal, backref="lote", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Nota Fiscal: {self.numero_serie}>"