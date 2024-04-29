const API_BASE_URL = "https://data.zeromev.org/v1";

export interface IAddressMevData {
  mev_type: string;
  sum_user_loss_usd?: number;
  sum_user_swap_volume_usd?: number;
  sum_user_swap_count?: number;
  sum_extractor_profit_usd?: number;
  sum_extractor_swap_volume_usd?: number;
  sum_extractor_swap_count?: number;
}
export async function getMevSummarized(
  address: string
): Promise<IAddressMevData | undefined> {
  const response = (await fetch(
    `${API_BASE_URL}/mevTransactionsSummary?address_from=${address}`
  ).then((r) => r.json())) as IAddressMevData[];
  const sandwich_summary = response.find(
    (summary) => summary.mev_type === "sandwich"
  );
  return sandwich_summary;
}
