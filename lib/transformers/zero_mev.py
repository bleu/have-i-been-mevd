from collections import defaultdict
from dataclasses import dataclass
from typing import List

from lib.zero_mev_api.models import MevTransaction


@dataclass
class ScanAddressData:
    address: str
    total_amount_usd: float
    mev_txs_length: int
    most_mev_protocol_name: str
    most_mev_protocol_usd_amount: float


@dataclass
class MostMevProtocol:
    name: str
    total_amount: float


def filter_mev_transactions_with_user_loss(
    mev_transactions: List[MevTransaction],
) -> List[MevTransaction]:
    return [tx for tx in mev_transactions if tx.user_loss_usd]


def get_scan_address_data_from_mev_transactions(
    mev_transactions: List[MevTransaction], address: str
) -> ScanAddressData:
    for tx in mev_transactions:
        tx.user_loss_usd = tx.user_loss_usd * -1  # type: ignore user loss usd is negative
    total_amount_usd = sum([tx.user_loss_usd for tx in mev_transactions])  # type: ignore
    most_mev_protocol = find_largest_mev_transaction_protocol(mev_transactions)
    return ScanAddressData(
        address=address,
        total_amount_usd=total_amount_usd,
        mev_txs_length=len(mev_transactions),
        most_mev_protocol_name=most_mev_protocol.name,
        most_mev_protocol_usd_amount=most_mev_protocol.total_amount,
    )


def find_largest_mev_transaction_protocol(
    mev_transactions: List[MevTransaction],
) -> MostMevProtocol:
    totals = defaultdict(int)
    mev_transaction_with_protocol = [tx for tx in mev_transactions if tx.protocol]

    for tx in mev_transaction_with_protocol:
        type_key = tx.protocol
        totals[type_key] += tx.user_loss_usd  # type: ignore

    max_type = max(totals, key=totals.get)  # type: ignore

    return MostMevProtocol(name=max_type, total_amount=totals[max_type])


def get_total_extracted_amount(mev_transactions: List[MevTransaction]) -> float:
    return sum([tx.user_loss_usd * -1 for tx in mev_transactions if tx.user_loss_usd])


def get_total_profit_amount(mev_transactions: List[MevTransaction]) -> float:
    return sum(
        [tx.extractor_profit_usd for tx in mev_transactions if tx.extractor_profit_usd]
    )


def get_total_victims_number(mev_transactions: List[MevTransaction]) -> int:
    return len(set([tx.address_from for tx in mev_transactions]))
