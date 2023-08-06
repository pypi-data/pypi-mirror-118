"""Contains the classes and methods used to
interact with thune money trnasfer api
"""
from typing import Any, Dict
import requests
from requests.auth import HTTPBasicAuth
from requests.models import Response


class Thunes:
    """A wrapper for Thunes money transfer API
    """
    __base_url: str = 'https://api-mt.pre.thunes.com'
    __urls = {
        'create_quotation': '/quotations',
        'create_transaction': '/quotations/%s/transactions',
        'add_attachments': '/transactions/%s/attachments',
        'services': '/services',
        'payers': '/payers',
        'payer': '/payers/%s',
        'payer_rates': '/payers/%s/rates',
        'countries': '/countries',
        'lookups': '/lookups/BIC/%s',
        'balances': '/balances',
        'ping': '/ping'
    }

    def __init__(self, api_key: str, api_secret: str):
        self.__api_key: str = api_key
        self.__api_secret: str = api_secret
        self.__base_url: str = 'https://api-mt.pre.thunes.com'

    # pylint: disable=too-many-arguments
    def create_quotation(self, external_id: str,
                         payer_id: str,
                         mode: str,
                         transaction_type: str,
                         amount: str,
                         source_currency: str,
                         source_country_iso_code: str,
                         destination_currency: str) -> Response:
        """Creates a Quotation

        Args:
            external_id (str): External reference ID
            payer_id (str): Yes	Integer	Payer ID
            mode (str): Quotation mode
            transaction_type (str): Transaction type
            amount (str): the amount
            source_currency (str): The source currency
            source_country_iso_code (str): source country code
            destination_currency (str): destination currency

        Returns:
            Response: http response object
        """

        url: str = self.__urls['create_quotation']
        payload = {
            "external_id": external_id,
            "payer_id": payer_id,
            "mode": mode,
            "transaction_type": transaction_type,
            "source": {
                "currency": source_currency,
                "country_iso_code": source_country_iso_code
            },
            "destination": {
                "currency": destination_currency
            }
        }

        if mode == 'SOURCE_AMOUNT':
            payload['source']['amount'] = amount
        else:
            payload['destination']['amount'] = amount

        response = self.__post(url, payload=payload)
        return response

    def get_services(self) -> Response:
        """Retrieves a list of all services available to the caller.

        Returns:
            Response: http response object
        """
        url: str = self.__urls['services']
        return self.__get(url)

    def get_payers(self) -> Response:
        """Retrieves a list of all payers available for the caller

        Returns:
            Response: Http response with a list of payers
        """
        url: str = self.__urls['payers']
        return self.__get(url)

    def get_payer(self, payer_id: int) -> Response:
        """Retrieve information for a given payer id

        Args:
            payer_id (int): The payer unique identifier

        Returns:
            Response: Http response with the payer data
        """
        url: str = self.__urls['payer'] % payer_id
        return self.__get(url)

    def get_payer_rates(self, payer_id: int) -> Response:
        """Retrieve rates for a given payer

        Args:
            payer_id (int): The payer unique identifier

        Returns:
            Response: Http response with the payer rates
        """
        url: str = self.__urls['payer_rates'] % payer_id
        return self.__get(url)

    def get_countries(self) -> Response:
        """Retrieve list of countries for all money
        transfer services available for the caller.

        Returns:
            Response: [description]
        """
        url: str = self.__urls['countries']
        return self.__get(url)

    def lookups(self, swift: str) -> Response:
        """Retrieve list of payers’ identifier for a given SWIFT BIC code

        Available for selected countries only

        Args:
            swift (str): SWIFT BIC code

        Returns:
            Response: Http response with list of payers
        """
        url: str = self.__urls['lookups'] % swift
        return self.__get(url)

    def balances(self) -> Response:
        """Retrieve information for all account balances per currency

        Returns:
            Response: List of balances
        """
        url: str = '/balances'
        return self.__get(url)

    def get(self, url: str, params: Dict[str, Any] = None) -> Response:
        """Performs a get request

        Provided a url and optional query params

        Args:
            url (str): a Thunes money transfer action to executed
                to call '/v2/money-transfer/quotations'
                simply use '/quotations'
            params (Dict[str, Any], optional): the query params.
                Defaults to None.

        Returns:
            Response: a response object
        """
        return self.__call('get', url, params=params)

    def post(self, url: str, payload: 'dict[str, Any]') -> Response:
        """Performs a post rquest to thunes money transfer api

        Args:
            url (str): a Thunes money transfer action to executed
                to call '/v2/money-transfer/quotations'
                simply use '/quotations'
            payload (dict[str, Any]): a json like object to be posted

        Returns:
            Response: An HTTP response object
        """
        return self.__call('post', url, payload=payload)

    def __auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.__api_key, self.__api_secret)

    def __get(self, url: str) -> Response:
        return self.__call('get', url)

    def __post(self, url: str, payload: 'dict[str, Any]') -> Response:
        return self.__call('post', url, payload=payload)

    def __call(self, action: str, url: str,
               payload: 'dict[str, Any]' = None,
               params: Dict[str, Any] = None) -> Response:
        auth: HTTPBasicAuth = self.__auth()
        url = self.__base_url + '/v2/money-transfer' + url
        if payload:
            return requests.request(
                action, url, json=payload,
                auth=auth, verify=False, params=params)

        return requests.request(
            action, url, auth=auth, verify=False)

    def __repr__(self):
        return f"Thunes({self.__api_key!r}, {self.__api_secret!r})"

    def __str__(self):
        return f"Thunes {self.__api_key} {self.__api_secret})"
