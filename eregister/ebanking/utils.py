from dateutil.parser import parse
import hashlib
import base64


def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return string
    except ValueError:
        return None


def generate_sha256(input_string):
    hash_object = hashlib.sha256(input_string.encode())
    output = hash_object.hexdigest()
    return output


def decode_base64(encoded_b64_input):
    return str(base64.b64decode(encoded_b64_input).decode('utf-8'))


def encode_base64(input_str):
    encodedBytes = base64.b64encode(input_str.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    return encodedStr
