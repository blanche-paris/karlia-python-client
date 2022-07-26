from __future__ import annotations

from typing import Any

import httpx

from .interfaces import Customer

customer_custom_field_map = {
    "category": 14627,
    "wedding_date": 15013,
    "budget": 15014,
    "wedding_place": 15015,
}

customer_category_map = {
    "Mariée S/M": 27673,
    "Civil": 27672,
}

pipeline_map = {
    "Mariées": 2586,
    "wholesale": 2869,
}


async def _hook_raise_for_status(response: httpx.Response) -> httpx.Response:
    response.raise_for_status()
    return response


class Client(httpx.AsyncClient):
    def __init__(
        self,
        token: str,
        base_url: str = "https://karlia.fr/app/api/v2",
        **kwargs: Any,
    ):
        headers = kwargs.get("headers", {})
        headers.update({"Authorization": f"Bearer {token}"})

        event_hooks = kwargs.get("event_hooks", {"response": [_hook_raise_for_status]})

        super().__init__(
            base_url=base_url, headers=headers, event_hooks=event_hooks, **kwargs
        )

    async def get_customers(self, offset: int = 0) -> list[Customer]:
        resp = await self.get("/customers", params={"offset": offset})
        return [Customer(**e) for e in resp.json()["data"]]

    # def get_all_opportunities(self):
    #     resp = self.get("/opportunities")
    #     resp.raise_for_status()
    #     return resp.json()["data"]

    # def get_customer_by_email(self, email: str):
    #     resp = self.get("/customers", params={"email": email})
    #     resp.raise_for_status()
    #     data = resp.json()["data"]
    #     if len(data) == 1:
    #         return data[0]
    #     elif len(data) == 0:
    #         return None
    #     else:
    #         raise ValueError("multiple clients found")

    # def get_opportunities_by_email(self, email: str):
    #     customer = self.get_customer_by_email(email=email)
    #     if not customer:
    #         return None
    #     resp = self.get(
    #         "/opportunities", params={"id_customer_supplier": int(customer["id"])}
    #     )
    #     resp.raise_for_status()
    #     return resp.json()["data"]

    # def create_customer(
    #     self,
    #     firstname: str,
    #     name: str,
    #     email: str,
    #     phone: str,
    #     is_prospect: bool,
    #     custom_fields: dict,
    #     **kwargs,
    # ) -> None:
    #     data = dict(
    #         name=name,
    #         email=email,
    #         firstname=firstname,
    #         individual=1,
    #         id_civility=2,
    #         prospect=int(is_prospect),
    #         phone=phone,
    #         langId=1,
    #         custom_fields=[
    #             dict(id=customer_custom_field_map[k], value=v)
    #             for k, v in custom_fields.items()
    #         ],
    #     )
    #     data = data | kwargs
    #     resp = self.post("/customers", body=data)
    #     resp.raise_for_status()
    #     return resp.json()
