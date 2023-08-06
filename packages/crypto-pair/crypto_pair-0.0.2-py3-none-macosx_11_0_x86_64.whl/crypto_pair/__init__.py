from typing import Optional

from crypto_pair._lowlevel import ffi, lib


def normalize_pair(symbol: str, exchange: str) -> Optional[str]:
    string_ptr = lib.normalize_pair(
        ffi.new("char[]", symbol.encode("utf-8")),
        ffi.new("char[]", exchange.encode("utf-8")),
    )
    if string_ptr == ffi.NULL:
        return None
    try:
        # Copy the data to a python string
        return ffi.string(string_ptr).decode('UTF-8')
    finally:
        lib.deallocate_string(string_ptr)
