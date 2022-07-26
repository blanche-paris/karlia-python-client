from __future__ import annotations

from datetime import datetime
from typing import Any

import pydantic


class Address(pydantic.BaseModel):
    pass


class Customer(pydantic.BaseModel):
    address_list: list[Address]  # [],
    client_number: str  # '',
    created_by: int  # '2388',
    creation_date: datetime  # '2022-03-09 15:33:40',
    custom_fields_list: list[Any]  # [],
    description: str  # '',
    email: str  # '',
    id: int  # '187522',
    id_client_manager: list[str]  # ['u2388'],
    id_parent: int  # '0',
    id_payment_condition: int  # '0',
    id_products_prices_category: int  # '0',
    id_vat: int  # '-1',
    individual: int  # '0',
    langId: int  # '1',
    legal_form: str  # '',
    main_activity: str  # '',
    mobile: str  # '',
    phone: str  # '+33123456789',
    prospect: int  # '0',
    siren: str  # '',
    siret: str  # '',
    title: str  # 'Société Test 2',
    update_date: datetime  # '2022-03-09 15:34:01',
    updated_by: int  # '1',
    vat_number: str  # ''

    class Config:
        arbitrary_types_allowed = True
