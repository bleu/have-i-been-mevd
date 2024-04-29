import { Button } from "@bleu-fi/ui";

export const COW_SWAP_URL = "https://swap.cow.fi/";

export function TradeOnCoWButton() {
  return (
    <a
      target="_blank"
      rel="noopener noreferrer"
      href={COW_SWAP_URL}
      className="font-bold"
    >
      <Button className="rounded-full">Trade safely on CoW Swap</Button>
    </a>
  );
}
