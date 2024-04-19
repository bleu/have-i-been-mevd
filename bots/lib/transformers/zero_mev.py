from dataclasses import dataclass
import pandas as pd

@dataclass
class ScanAddressData:
    address: str
    total_amount_usd: float
    mev_txs_length: int
    most_mev_protocol_name: str
    most_mev_protocol_usd_amount: float


def minimal_preporcessing(mev_transactions: pd.DataFrame) -> pd.DataFrame:
    mev_transactions["user_loss_usd"] = abs(mev_transactions["user_loss_usd"])
    mev_transactions.dropna(subset=["user_loss_usd"], inplace=True)
    return mev_transactions


def get_scan_address_data_from_mev_transactions(
    mev_transactions: pd.DataFrame, address: str
) -> ScanAddressData:
    total_amount_usd = mev_transactions["user_loss_usd"].sum()
    mev_by_protocol = mev_transactions.groupby("protocol")["user_loss_usd"].sum()
    most_mev_protocol_name = str(mev_by_protocol.idxmax())
    most_mev_protocol_usd_amount = float(mev_by_protocol.max())
    mev_txs_length = int(mev_transactions["user_loss_usd"].count())

    return ScanAddressData(
        address=address,
        total_amount_usd=total_amount_usd,
        mev_txs_length=mev_txs_length,
        most_mev_protocol_name=most_mev_protocol_name,
        most_mev_protocol_usd_amount=most_mev_protocol_usd_amount,
    )
