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


@dataclass
class OverviewData:
    mev_swaps_number: int
    mev_extracted_amount: float
    mev_profit_amount: float
    mev_victims_number: int


def filter_mev_transactions_with_user_loss(
    mev_transactions: List[MevTransaction],
) -> List[MevTransaction]:
    return [tx for tx in mev_transactions if tx.user_loss_usd]


def get_scan_address_data_from_mev_transactions(
    mev_transactions: List[MevTransaction], address: str
) -> ScanAddressData:
    for tx in mev_transactions:
        tx.user_loss_usd = tx.user_loss_usd * -1  # user loss usd is negative
    total_amount_usd = sum([tx.user_loss_usd for tx in mev_transactions])
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
        totals[type_key] += tx.user_loss_usd

    max_type = max(totals, key=totals.get)

    return MostMevProtocol(name=max_type, total_amount=totals[max_type])


def get_overview_data_from_mev_transactions(
    mev_transactions: List[MevTransaction],
) -> OverviewData:
    mev_swaps_number = len(
        [
            tx.mev_type == "frontrun" or tx.mev_type == "sandwich"
            for tx in mev_transactions
        ]
    )
    mev_extracted_amount = (
        sum([tx.user_loss_usd for tx in mev_transactions if tx.user_loss_usd])
        * -1  # user loss usd is negative
    )

    mev_profit_amount = sum(
        [tx.extractor_profit_usd for tx in mev_transactions if tx.extractor_profit_usd]
    )

    mev_victims_number = len(set([tx.address_from for tx in mev_transactions]))

    return OverviewData(
        mev_swaps_number=mev_swaps_number,
        mev_extracted_amount=mev_extracted_amount,
        mev_profit_amount=mev_profit_amount,
        mev_victims_number=mev_victims_number,
    )
