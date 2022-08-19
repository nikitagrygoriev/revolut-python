import datetime
import dateutil.parser
from decimal import Decimal
import json
import jwt
import sys

if sys.version_info < (3,):  # pragma: nocover
    _integer_types = (
        int,
        long,
    )
    _str_types = (str, bytes, unicode)
else:  # pragma: nocover
    _integer_types = (int,)
    _str_types = (str, bytes)


def _obj2id(obj):
    return obj.id if hasattr(obj, "id") else obj


def _date(v):
    if not isinstance(v, (datetime.date, datetime.datetime)):
        return dateutil.parser.parse(v).date()
    elif isinstance(v, datetime.datetime):
        return v.date()
    return v

def _datetime(v):
    print(f"Input value: {v}, input format {type(v)}")
    if not isinstance(v, (datetime.date, datetime.datetime)):
        return dateutil.parser.parse(v).date().strftime('%Y-%m-%dT%H:%M:%S.%f%zZ')
    elif isinstance(v, datetime.datetime):
        return v.date().strftime('%Y-%m-%dT%H:%M:%S.%f%zZ')
    return v.strftime('%Y-%m-%dT%H:%M:%S.%f%zZ')

def _integertomoney(value_int):
    return (Decimal(value_int) / Decimal(100)).quantize(Decimal("0.01"))

class _SetEnv(object):
    def _set_env(self, token):
        if token.startswith("oa_prod"):
            self.base_url = "https://b2b.revolut.com/api/1.0/"
            self.live = True
        elif token.startswith("oa_sand"):
            self.base_url = "https://sandbox-b2b.revolut.com/api/1.0/"
            self.live = False
        elif token.startswith("sk_y"):
            self.base_url = "https://merchant.revolut.com/api/1.0/"
        elif token.startswith("sk_q"):
            self.base_url = "https://sandbox-merchant.revolut.com/api/1.0/"
        else:
            raise ValueError(
                "Token '{:s}' matches neither production nor sandbox environment.".format(
                    token
                )
            )


class JSONWithDecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(JSONWithDecimalEncoder, self).default(o)


def get_jwt(prvkey, issuer, client_id):
    """Generates JWT signed with the private key"""
    return jwt.encode(
        {"iss": issuer, "sub": client_id, "aud": "https://revolut.com"},
        prvkey,
        algorithm=("RS256"),
    )
