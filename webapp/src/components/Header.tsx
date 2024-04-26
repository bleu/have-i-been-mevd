import { truncateAddress } from "#/utils/truncateAddress";
import { Button } from "@bleu-fi/ui";
import { Address } from "viem";

export function Header({ address }: { address?: Address }) {
  return (
    <div className="flex flex-row w-full justify-between items-center border-b-2 border-primary py-2">
      <span className="text-xl font-bold">HAVE I BEEN MEV'D?</span>
      {address ? (
        <Button shade="dark">{truncateAddress(address)}</Button>
      ) : (
        <span className="text-md text-info">Not connected</span>
      )}
    </div>
  );
}
