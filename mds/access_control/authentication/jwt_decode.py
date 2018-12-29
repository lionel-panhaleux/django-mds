from typing import List, Dict

import jwt


def jwt_multi_decode(
    public_keys: List[str], secret_keys: List[str], encoded_jwt: str
) -> Dict:
    """
    Try all available secret and public keys to decode the JWT
    """

    assert public_keys or secret_keys, "At least one JWT key must be provided"

    exception_holder = jwt.InvalidSignatureError()

    header = jwt.get_unverified_header(encoded_jwt)
    alg = header["alg"]

    if alg == "RS256":
        # Instead of trying all certificates, we could use the 'kid' header to select the correct certificate
        for public_key in public_keys:
            try:
                return jwt.decode(encoded_jwt, public_key, algorithms="RS256")
            except jwt.InvalidSignatureError as e:
                exception_holder = e
    else:
        for secret_key in secret_keys:
            try:
                return jwt.decode(encoded_jwt, secret_key, algorithms="HS256")
            except jwt.InvalidSignatureError as e:
                exception_holder = e

    raise exception_holder
