from .models import Console
from ..extensions import ma

class ConsoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Console
