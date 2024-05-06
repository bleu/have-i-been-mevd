import { Address } from "viem";

const API_BASE_URL = "https://data.zeromev.org/v1";

export interface IAddressMevData {
  address: Address;
  totalAmountUsd: number;
  mevTxsLength: number;
  mostMevProtocolName: string;
  mostMevProtocolUsdAmount: number;
}

export interface IMevTransaction {
  block_number: number;
  tx_index: number;
  mev_type: string;
  protocol?: string;
  user_loss_usd?: number;
  extractor_profit_usd?: number;
  user_swap_volume_usd?: number;
  user_swap_count?: number;
  extractor_swap_volume_usd?: number;
  extractor_swap_count?: number;
  imbalance?: number;
  address_from?: string;
  address_to?: string;
  arrival_time_us?: string;
  arrival_time_eu?: string;
  arrival_time_as?: string;
}

export async function scanAddressMEV(
  address: Address
): Promise<IAddressMevData> {
  const mevTxs = await getPaginatedMevTransactionsByAddressAndKey(
    address,
    "address_from"
  );

  const sandwichTxs = mevTxs.filter((tx) => tx.mev_type === "sandwich");

  const totalAmountUsd = sandwichTxs.reduce(
    (acc, tx) => acc + Math.abs(tx.user_loss_usd || 0),
    0
  );

  const sumUserLossesByProtocol = (transactions: IMevTransaction[]) => {
    return transactions
      .filter(
        (tx) => tx.protocol !== undefined && tx.user_loss_usd !== undefined
      )
      .reduce((acc, curr) => {
        acc.set(
          curr.protocol || "",
          (acc.get(curr.protocol || "") || 0) +
            Math.abs(curr.user_loss_usd || 0)
        );
        return acc;
      }, new Map<string, number>());
  };

  const mev_by_protocol = sumUserLossesByProtocol(sandwichTxs);

  const [most_mev_protocol_name, most_mev_protocol_usd_amount] = Array.from(
    mev_by_protocol.entries()
  ).reduce(
    (acc, curr) => {
      return curr[1] > acc[1] ? curr : acc;
    },
    ["", 0]
  );

  return {
    address,
    totalAmountUsd,
    mevTxsLength: sandwichTxs.length,
    mostMevProtocolName: most_mev_protocol_name,
    mostMevProtocolUsdAmount: most_mev_protocol_usd_amount,
  };
}

async function getPaginatedMevTransactionsByAddressAndKey(
  address: string,
  paramsAddressKey: "address_from" | "address_to"
): Promise<IMevTransaction[]> {
  const params = {
    [paramsAddressKey]: address,
    page: 1,
  };
  const allData: IMevTransaction[] = [];
  let hasNextPage = true;

  while (hasNextPage) {
    // @ts-ignore
    const queryParams = new URLSearchParams(params).toString();
    const response = await fetch(
      `${API_BASE_URL}/mevTransactions?${queryParams}`
    );
    const data = await response.json();
    allData.push(...data);
    hasNextPage = data.length === 1000;
    params.page += 1;
  }

  return allData;
}
