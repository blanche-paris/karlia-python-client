from vcr import VCR

from karlia.client import Client


class TestCustomers:
    async def test_it_can_get_customers(self, vcr: VCR, client: Client):
        with vcr.use_cassette("get_customers.yaml"):
            customers = await client.get_customers()

        assert len(customers) == 100
