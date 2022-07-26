from vcr import VCR

from karlia_python_client.client import Client


class TestCustomers:
    async def test_it_can_get_customers(self, vcr: VCR, client: Client):
        with vcr.use_cassette("get_customers.yaml"):
            content = await client.get_customers()

        assert len(content["data"]) == 100

    async def test_it_can_get_single_customer_by_email(self, vcr: VCR, client: Client):
        with vcr.use_cassette("get_customer_by_email.yaml"):
            content = await client.get_customer_by_email("z.merlin@hotmail.fr")
        assert content


class TestOpportunities:
    async def test_it_can_get_opportunities(self, vcr: VCR, client: Client):
        with vcr.use_cassette("get_customers.yaml"):
            content = await client.get_customers()

        assert len(content["data"]) == 100
