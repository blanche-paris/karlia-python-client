from __future__ import annotations

from typing import Any

import httpx

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

    # _____ Customers _____

    async def get_customers(self, **params: Any) -> dict[str, Any]:
        resp = await self.get("/customers", params=params)
        return resp.json()  # type: ignore

    async def get_customer_by_email(self, email: str) -> dict[str, Any] | None:
        resp = await self.get("/customers", params={"email": email})
        data: list[dict[str, Any]] = resp.json()["data"]
        if len(data) == 1:
            return data[0]
        elif len(data) == 0:
            return None
        else:
            raise ValueError(f"Multiple customer for email '{email}")

    async def create_customer(
        self,
        firstname: str,
        name: str,
        email: str,
        phone: str,
        is_prospect: bool,
        custom_fields: dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        data = dict(
            name=name,
            email=email,
            firstname=firstname,
            individual=1,
            id_civility=2,
            prospect=int(is_prospect),
            phone=phone,
            langId=1,
            custom_fields=[
                dict(id=customer_custom_field_map[k], value=v)
                for k, v in custom_fields.items()
            ],
        )
        data = data | kwargs
        resp = await self.post("/customers", data=data)
        return resp.json()

    # _____ Opportunities _____

    async def get_opportunities(self) -> dict[str, Any]:
        resp = await self.get("/opportunities")
        return resp.json()  # type: ignore

    async def get_opportunities_by_email(self, email: str) -> dict[str, Any] | None:
        customer = await self.get_customer_by_email(email=email)
        if not customer:
            return None

        resp = self.get(
            "/opportunities", params={"id_customer_supplier": int(customer["id"])}
        )

        return resp.json()["data"]  # type: ignore
