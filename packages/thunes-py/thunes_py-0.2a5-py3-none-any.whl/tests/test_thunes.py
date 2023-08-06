# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use

from typing import Dict, List
import uuid
import os
import pytest
from thunes.thunes import Thunes


class TestThunes:
    # pylint: disable=missing-class-docstring
    @pytest.fixture
    def api_key(self):
        return os.getenv('API_KEY')

    @pytest.fixture
    def api_secret(self):
        return os.getenv('API_SECRET')

    @pytest.fixture
    def thunes(self, api_key, api_secret):
        return Thunes(api_key, api_secret)

    def test_get_payers(self, thunes: Thunes):
        response = thunes.get_payers()
        payers: List[Dict[str, any]] = response.json()

        assert isinstance(payers, list)

    def test_should_get_payer(self, thunes: Thunes):
        response = thunes.get_payer(42)
        payer: Dict[str, any] = response.json()

        assert payer['id'] == 42

    def test_should_get_payer_rates(self, thunes: Thunes):
        response = thunes.get_payer_rates(42)
        rates: Dict[str, any] = response.json()

        assert rates['destination_currency'] == 'KES'

    def test_create_quotation(self, thunes: Thunes):
        external_id: str = str(uuid.uuid4())
        payer_id: int = 42
        mode: str = "SOURCE_AMOUNT"
        transaction_type: str = "C2C"
        amount: str = "100"
        source_currency: str = "SGD"
        source_country_iso_code: str = "KEN"
        destination_currency: str = "KES"
        response = thunes.create_quotation(
            external_id=external_id,
            payer_id=payer_id,
            mode=mode,
            transaction_type=transaction_type,
            amount=amount,
            source_currency=source_currency,
            source_country_iso_code=source_country_iso_code,
            destination_currency=destination_currency)
        quotation: dict = response.json()

        assert quotation['transaction_type'] == 'C2C'

    def test_get_balances(self, thunes: Thunes):
        response = thunes.balances()
        balances = response.json()

        assert isinstance(balances, list)

    def test_get_services(self, thunes: Thunes):
        response = thunes.get_services()
        services = response.json()

        assert isinstance(services, list)

    def test_get_countries(self, thunes: Thunes):
        response = thunes.get_countries()
        countries: List[Dict[str, any]] = response.json()

        assert isinstance(countries, list)

    def test_lookups(self, thunes: Thunes):
        response = thunes.lookups('BARCGHAC')
        lookups: List[Dict[str, any]] = response.json()

        assert isinstance(lookups, list)

    def test_lookups_with_get(self, thunes: Thunes):
        response = thunes.get("/lookups/BIC/BARCGHAC")
        lookups: List[Dict[str, any]] = response.json()

        assert isinstance(lookups, list)

    def test_create_quotation_with_post(self, thunes: Thunes):
        payload = {
            'external_id': str(uuid.uuid4()),
            'payer_id': 42, 'mode': 'SOURCE_AMOUNT',
            'transaction_type': 'C2C',
            'source': {
                'amount': 12323.33,
                'currency': 'SGD',
                'country_iso_code': 'KEN'
            },
            'destination': {
                'currency': 'KES'
            }
        }
        response = thunes.post("/quotations", payload=payload)
        quotation: dict = response.json()
        assert quotation['transaction_type'] == 'C2C'
