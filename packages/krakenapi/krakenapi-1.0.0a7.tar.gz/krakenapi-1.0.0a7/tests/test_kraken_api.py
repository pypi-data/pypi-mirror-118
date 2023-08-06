from krakenapi import KrakenApi
from freezegun import freeze_time
import pytest
from urllib.request import Request
import vcr
from .fixtures import trades

fake_public_key = "R6/OvXmIQEv1E8nyJd7+a9Zmaf84yJ7uifwe2yj5BgV1N+lgqURsxQwQ"
fake_private_key = "MWZ9lFF/mreK4Fdk/SEpFLvVn//nbKUbCytGShSwvCvYlgRkn4K8i7VY18UQEgOHzBIEsqg78BZJCEhvFIzw1Q=="


class TestKrakenAPI:
    # KrakenAPI object for public API endpoints.
    ka_public: KrakenApi
    # KrakenAPI object for private API endpoints - Fake keys.
    ka_private: KrakenApi

    def setup(self):
        self.ka_public = KrakenApi("api_public_key", "api_private_key")
        self.ka_private = KrakenApi(
            fake_public_key,
            fake_private_key,
        )

    def test_init(self):
        assert type(self.ka_public) == KrakenApi
        assert self.ka_public.api_public_key == "api_public_key"
        assert self.ka_public.api_private_key == "api_private_key"

        assert type(self.ka_private) == KrakenApi
        assert self.ka_private.api_public_key == fake_public_key
        assert self.ka_private.api_private_key == fake_private_key

    def test_create_api_path(self):
        # Test public API endpoint path.
        api_path = self.ka_public.create_api_path(True, "Time")
        assert api_path == "https://api.kraken.com/0/public/Time"

        # Test private API endpoint path.
        api_path = self.ka_public.create_api_path(False, "Balance")
        assert api_path == "https://api.kraken.com/0/private/Balance"

    @freeze_time("2012-01-13 23:10:34.069731")
    def test_create_api_nonce(self):
        api_nonce = self.ka_public.create_api_nonce()
        assert api_nonce == "1326496234069"

    def test_create_api_post_data(self):
        # Test with post inputs and api nonce.
        post_inputs = {"start": 1617753600, "closetime": "open"}
        api_nonce = "1326496234069"
        api_post_data = self.ka_public.create_api_post_data(post_inputs, api_nonce)
        assert api_post_data == b"start=1617753600&closetime=open&nonce=1326496234069"

        # Test with only post inputs.
        post_inputs = {"pair": "XETHZEUR"}
        api_post_data = self.ka_public.create_api_post_data(post_inputs)
        assert api_post_data == b"pair=XETHZEUR"

        # Test with only api_nonce.
        api_nonce = "1617824500528"
        api_post_data = self.ka_public.create_api_post_data(None, api_nonce)
        assert api_post_data == b"nonce=1617824500528"

        # Should raise a TypeError if post inputs and api nonce are missing.
        with pytest.raises(TypeError) as e_info:
            self.ka_public.create_api_post_data()
        assert "API Post with missing post inputs and nonce ->" in str(e_info.value)

    def test_create_api_signature(self):
        api_nonce = "1617828062628"

        # Test signature with method with only nonce as parameters,
        # using an incorrectly and correctly formatted API keys.
        api_method = "TradeBalance"
        api_post_data = b"nonce=1617828062628"
        with pytest.raises(ValueError) as e_info:
            self.ka_public.create_api_signature(api_nonce, api_post_data, api_method)
        assert "Incorrect Kraken API private key ->" in str(e_info.value)
        api_signature = self.ka_private.create_api_signature(
            api_nonce, api_post_data, api_method
        )
        correct_api_signature = "Q7QwKIQu+8wlTtkcF2vwkPFkAP+10diymNsOIoOy+x1PoSUJFz5SAg5TRrvoBlzrgA9oxqjOWcAFqvqcarJZ3w=="
        assert api_signature == correct_api_signature

        # Test signature with method using start,
        # closedtime and nonce as parameters.
        api_method = "ClosedOrders"
        api_post_data = b"start=1617753600&closetime=open&nonce=1617828329075"
        api_signature = self.ka_private.create_api_signature(
            api_nonce, api_post_data, api_method
        )
        correct_api_signature = "RsNkND1GcQmKpayw/o3CJzWheC8dYxyEjWXtha0tPqQVzfLOxtpyd2zLM4vB8ajFqTmO/GXkoqzmkwTJxNAHcw=="
        assert api_signature == correct_api_signature

        # Test signature with method using pair, type,
        # ordertype, price, volume and nonce as parameters.
        api_method = "AddOrder"
        api_post_data = b"pair=XETHZUSD&type=buy&ordertype=limit&price=1985.42&volume=0.00755507&nonce=1617828386991"
        api_signature = self.ka_private.create_api_signature(
            api_nonce, api_post_data, api_method
        )
        correct_api_signature = "q5vxW9cvCBY5kmCfjl0JC8/cQeEaKM4i4vprNsqmyd9jshoB0cybg7IRddYEkxdBKxQF/ima/InTjJUJgQMnIg=="
        assert api_signature == correct_api_signature

    def test_extract_response_data(self):
        # Raise error when wrong data format received.
        data = b"Wrong data"
        with pytest.raises(ValueError) as e_info:
            self.ka_public.extract_response_data(data)
        assert "Response received from API was wrongly formatted ->" in str(
            e_info.value
        )

        # Test extract data from Kraken API as dict from bytes
        # with format {"error": list, result: dit}.
        data = b'{"error":[],"result":{"unixtime":1617831335,"rfc1123":"Wed,  7 Apr 21 21:35:35 +0000"}}'
        data = self.ka_public.extract_response_data(data)
        correct_data = {
            "unixtime": 1617831335,
            "rfc1123": "Wed,  7 Apr 21 21:35:35 +0000",
        }
        assert data == correct_data

        # Extract error message when received one.
        data = b'{"error":["EOrder:Insufficient funds"]}'
        data = self.ka_public.extract_response_data(data)
        assert data == "EOrder:Insufficient funds"

    @freeze_time("2012-01-13 23:10:34.069731")
    def test_create_api_request(self):
        # Test from public method with post inputs.
        post_inputs = {"pair": "XETHZUSD"}
        request = self.ka_public.create_api_request(True, "Ticker", post_inputs)
        assert type(request) == Request
        assert request.data == b"pair=XETHZUSD"
        assert request.full_url == "https://api.kraken.com/0/public/Ticker"
        assert request.host == "api.kraken.com"
        assert request.origin_req_host == "api.kraken.com"
        assert request.selector == "/0/public/Ticker"
        assert request.type == "https"

        # Test from public method without post inputs.
        request = self.ka_public.create_api_request(True, "Time")
        assert type(request) == Request
        assert request.data is None
        assert request.full_url == "https://api.kraken.com/0/public/Time"
        assert request.host == "api.kraken.com"
        assert request.origin_req_host == "api.kraken.com"
        assert request.selector == "/0/public/Time"
        assert request.type == "https"

        # Test from private method with post inputs.
        post_inputs = {"pair": "XETHZUSD"}
        request = self.ka_private.create_api_request(False, "ClosedOrders", post_inputs)
        assert type(request) == Request
        assert request.data == b"pair=XETHZUSD&nonce=1326496234069"
        assert request.full_url == "https://api.kraken.com/0/private/ClosedOrders"
        assert request.host == "api.kraken.com"
        assert request.origin_req_host == "api.kraken.com"
        assert request.selector == "/0/private/ClosedOrders"
        assert request.type == "https"
        api_sign = "UTq1QrYgqyXh7pa4UtSVeGe28oCcOMUci0CA3j8bQ+S5nvs7PDhUklSdfmjYd+qBbnEH9BGsKUEksRQFQOkS6w=="
        assert request.headers.get("Api-sign") == api_sign
        api_key = "R6/OvXmIQEv1E8nyJd7+a9Zmaf84yJ7uifwe2yj5BgV1N+lgqURsxQwQ"
        assert request.headers.get("Api-key") == api_key

        # Test from private method without post inputs.
        request = self.ka_private.create_api_request(False, "TradeBalance")
        assert type(request) == Request
        assert request.data == b"nonce=1326496234069"
        assert request.full_url == "https://api.kraken.com/0/private/TradeBalance"
        assert request.host == "api.kraken.com"
        assert request.origin_req_host == "api.kraken.com"
        assert request.selector == "/0/private/TradeBalance"
        assert request.type == "https"
        api_sign = "o4flfJB00EwybhqfMjQ0LFnGp88pTpW1gN5xNDfIATu59sD5TsxeVHND9wH5Wq2vdA9qGF1idb5wnF4QVuvU6Q=="
        assert request.headers.get("Api-sign") == api_sign
        api_key = "R6/OvXmIQEv1E8nyJd7+a9Zmaf84yJ7uifwe2yj5BgV1N+lgqURsxQwQ"
        assert request.headers.get("Api-key") == api_key

    def test_send_api_request(self):
        # Test valid request
        request = self.ka_public.create_api_request(True, "Time")
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_time.yaml"):
            data = self.ka_public.send_api_request(request)
        assert type(data) == dict
        assert data.get("unixtime") == 1618001260
        assert data.get("rfc1123") == "Fri,  9 Apr 21 20:47:40 +0000"

        # Test error raising
        with vcr.use_cassette(
            "tests/fixtures/vcr_cassettes/test_create_order_error.yaml",
            filter_headers=["API-Key", "API-Sign"],
        ):
            with pytest.raises(ValueError) as e_info:
                self.ka_private.create_order(
                    "XETHZEUR", "buy", "limit", 1960.86, 1, "fciq"
                )
        error_message = "Kraken API error -> EOrder:Insufficient funds"
        assert error_message in str(e_info.value)

    @vcr.use_cassette(
        "tests/fixtures/vcr_cassettes/test_get_assets.yaml",
        filter_headers=["API-Key", "API-Sign"],
    )
    def test_get_assets(self):
        data = self.ka_public.get_assets()
        assert type(data) == dict
        assert len(data) == 79
        for key, value in data.items():
            assert type(key) == str
            assert type(value) == dict

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_asset_pairs.yaml")
    def test_get_asset_pairs(self):
        data = self.ka_public.get_asset_pairs()
        assert type(data) == dict
        assert len(data) == 304
        for key, value in data.items():
            assert type(key) == str
            assert type(value) == dict

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_time.yaml")
    def test_get_time(self):
        data = self.ka_public.get_time()
        assert type(data) == int
        assert data == 1618001260

    def test_get_pair_ticker(self):
        # Test with existing pair.
        pair = "XETHZEUR"
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_pair_ticker.yaml"):
            data = self.ka_public.get_pair_ticker(pair)
        assert type(data) == dict
        key = next(iter(data))
        assert type(key) == str
        assert key == "XETHZEUR"
        value = next(iter(data.values()))
        assert type(value) == dict

        # Test with fake pair.
        pair = "Fake"
        with vcr.use_cassette(
            "tests/fixtures/vcr_cassettes/test_get_pair_ticker_error.yaml"
        ):
            with pytest.raises(ValueError) as e_info:
                self.ka_public.get_pair_ticker(pair)
        assert "Kraken API error -> EQuery:Unknown asset pair" in str(e_info.value)

    @vcr.use_cassette(
        "tests/fixtures/vcr_cassettes/test_get_balance.yaml",
        filter_headers=["API-Key", "API-Sign"],
    )
    def test_get_balance(self):
        data = self.ka_private.get_balance()
        assert type(data) == dict
        key = next(iter(data))
        assert type(key) == str
        assert key == "ZEUR"
        value = next(iter(data.values()))
        assert type(value) == str
        assert value == "60.0000"

    @vcr.use_cassette(
        "tests/fixtures/vcr_cassettes/test_get_trade_balance.yaml",
        filter_headers=["API-Key", "API-Sign"],
    )
    def test_get_trade_balance(self):
        data = self.ka_private.get_trade_balance()
        assert type(data) == dict
        correct_keys = ["eb", "tb", "m", "n", "c", "v", "e", "mf"]
        keys = list(data.keys())
        assert keys == correct_keys
        value = next(iter(data.values()))
        assert type(value) == str
        assert value == "197.0337"

    @vcr.use_cassette(
        "tests/fixtures/vcr_cassettes/test_get_open_orders.yaml",
        filter_headers=["API-Key", "API-Sign"],
    )
    def test_get_open_orders(self):
        data = self.ka_private.get_open_orders()
        assert type(data) == dict
        assert len(data) == 1
        key = next(iter(data))
        assert type(key) == str
        assert key == "O7JHTY-754IO-YU46NZ"
        value = next(iter(data.values()))
        assert type(value) == dict

    @vcr.use_cassette(
        "tests/fixtures/vcr_cassettes/test_get_closed_orders.yaml",
        filter_headers=["API-Key", "API-Sign"],
    )
    def test_get_closed_orders(self):
        data = self.ka_private.get_closed_orders()
        assert type(data) == dict
        assert len(data) == 1
        key = next(iter(data))
        assert type(key) == str
        assert key == "OPHJMI-YDCPY-POU4AJ"
        value = next(iter(data.values()))
        assert type(value) == dict

    @vcr.use_cassette(
        "tests/fixtures/vcr_cassettes/test_create_order.yaml",
        filter_headers=["API-Key", "API-Sign"],
    )
    def test_create_order(self):
        data = self.ka_private.create_order(
            "XETHZEUR", "buy", "limit", 1938.11, 0.01029256, "fciq"
        )
        assert type(data) == dict
        assert data == {
            "descr": {"order": "buy 0.01029256 ETHEUR @ limit 1938.11"},
            "txid": ["OUHXFN-RTP6W-ART4VP"],
        }

    @vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_trades.yaml")
    def test_get_trades_history(self, capfd):
        data = self.ka_public.get_trades_history("XBTEUR", 1619502600, 1619503200, True)
        assert type(data) == list
        assert data == trades
        captured = capfd.readouterr()
        test_output = "XBTEUR: Downloaded trades from 2021-04-27 05:50:00 to 2021-04-27 06:11:16.787426.\n"
        assert captured.out == test_output

    def test_get_asset_name(self):
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_assets.yaml"):
            with pytest.raises(ValueError) as e_info:
                self.ka_public.get_asset_altname("ETHXBT")
        assert "ETHXBT asset not available on Kraken." in str(e_info.value)
        with vcr.use_cassette("tests/fixtures/vcr_cassettes/test_get_assets.yaml"):
            altname = self.ka_public.get_asset_altname("XXBT")
        assert altname == "XBT"

