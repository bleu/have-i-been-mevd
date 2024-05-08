import json
import os
from functools import cache

import web3


@cache
def get_web3_provider():
    """Returns Web3 Provider"""
    return web3.Web3(
        web3.HTTPProvider(f"https://eth.llamarpc.com/rpc/01GYHXMVJ2H51X5M316Z8CYEXM")
    )


@cache
def get_web3_async_provider():
    """Returns Web3 Async Provider"""
    return web3.AsyncWeb3(
        web3.AsyncHTTPProvider(
            f"https://eth.llamarpc.com/rpc/01GYHXMVJ2H51X5M316Z8CYEXM"
        )
    )


@cache
def _get_contract_abi(abi_file_name):
    """Tries to fetch ABI json for provided file name"""
    file_path = os.path.join("bots", "lib", "w3", "abis", abi_file_name)
    with open(file_path) as f:
        return json.load(f)


@cache
def get_web3_contract(contract_address, abi_file_name):
    w3 = get_web3_async_provider()
    return w3.eth.contract(
        address=w3.to_checksum_address(contract_address),
        abi=_get_contract_abi(abi_file_name),
    )


def get_address(address_or_ens_name: str):
    """Get the address from the ENS name or address"""
    w3 = get_web3_provider()
    if w3.is_address(address_or_ens_name):
        return address_or_ens_name

    return w3.ens.address(address_or_ens_name)  # type: ignore
