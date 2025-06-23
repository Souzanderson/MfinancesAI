from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import mysql.connector
from settings import DATABASE_CONFIG

class Item(BaseModel):
    id: int | None = Field(default=None, alias="id")
    item: str = Field(..., alias="item")
    qtd: int = Field(..., alias="qtd")
    total: float = Field(..., alias="total")
    natureza: str = Field(..., alias="natureza")
    parcelado: bool = Field(..., alias="parcelado")
    parcelas: int = Field(None, alias="parcelas")
    parcela_atual: int = Field(None, alias="parcela_atual")
    valor_parcela_atual: float | None = Field(default=0.0, alias="valor_parcela_atual")
    date_create: datetime | None = Field(default=datetime.now(), alias="date_create")

    @staticmethod
    def from_json(data: dict):
        return Item(**data)
    
    @staticmethod
    def get_by_month_year(month: int, year: int, db_config: dict = DATABASE_CONFIG):
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM items
            WHERE MONTH(date_create) = %s AND YEAR(date_create) = %s
        """
        cursor.execute(query, (month, year))
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return [Item.from_json(row) for row in results]
    
    @staticmethod
    def get_receitas_despesas_by_month_year(month: int, year: int, db_config: dict = DATABASE_CONFIG ):
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT natureza, total, parcelas
            FROM items
            WHERE MONTH(date_create) = %s AND YEAR(date_create) = %s
        """
        cursor.execute(query, (month, year))
        results = cursor.fetchall()
        cursor.close()
        connection.close()

        receitas = sum(row["total"] / row["parcelas"] for row in results if row["natureza"] == "entrada" and row["parcelas"])
        despesas = sum(row["total"] / row["parcelas"] for row in results if row["natureza"] == "saida" and row["parcelas"])

        return {"receitas": receitas, "despesas": despesas, "month": month, "year": year}

    def distribuir_parcelas_e_inserir(self, db_config: dict = DATABASE_CONFIG):
        if not self.date_create:
            self.date_create = datetime.now()
        if self.parcelado and self.parcelas and self.parcelas > 1:
            parcela_data = self.date_create

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            items_parcelas = []
            for parcela in range(1, self.parcelas + 1):
                # A primeira parcela é no mês anterior, a segunda no mês atual, a terceira no próximo mês, etc.
                parcela_data = self.date_create + timedelta(days=30 * (parcela - self.parcela_atual))
                valor_parcela_atual = self.total / self.parcelas if self.parcelas > 0 else 0.0
                
                item_parcela = {
                    "item": self.item,
                    "qtd": self.qtd,
                    "total": self.total,
                    "natureza": self.natureza,
                    "parcelado": True,
                    "parcelas": self.parcelas,
                    "parcela_atual": parcela,
                    "valor_parcela_atual": valor_parcela_atual,
                    "date_create": parcela_data.strftime('%Y-%m-%d %H:%M:%S')
                }
                parcela_data += timedelta(days=30)  # Adiciona 30 dias para cada parcela
                items_parcelas.append(item_parcela)
                cursor.execute(
                    """
                    INSERT INTO items (item, qtd, total, natureza, parcelado, parcelas, parcela_atual, valor_parcela_atual, date_create)
                    VALUES (%(item)s, %(qtd)s, %(total)s, %(natureza)s, %(parcelado)s, %(parcelas)s, %(parcela_atual)s, %(valor_parcela_atual)s, %(date_create)s)
                    """,
                    item_parcela
                )

            connection.commit()
            cursor.close()
            connection.close()
            return items_parcelas
        else:
            # Insere o item diretamente no banco de dados
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            self.valor_parcela_atual = self.total 
            cursor.execute(
                    """
                    INSERT INTO items (item, qtd, total, natureza, parcelado, parcelas, parcela_atual, valor_parcela_atual, date_create)
                    VALUES (%(item)s, %(qtd)s, %(total)s, %(natureza)s, %(parcelado)s, %(parcelas)s, %(parcela_atual)s, %(valor_parcela_atual)s, %(date_create)s)
                    """,
                    self.dict()
                )
            connection.commit()
            cursor.close()
            connection.close()
            return [self.dict()]
            