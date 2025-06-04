from dataclasses import dataclass
from datetime import datetime
@dataclass
class Arco:
    order1_id: int
    order2_id: int
    order1_date: datetime
    order2_date: datetime
    qtyOrder: int