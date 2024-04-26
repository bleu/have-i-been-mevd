import { truncateAddress } from "#/utils/truncateAddress";
import { Address } from "viem";

export function Header({ address }: { address?: Address }) {
  return (
    <div className="flex flex-row w-full justify-between items-center border border-x-0 border-t-0 py-4">
      <span className="text-xl font-bold">HAVE I BEEN MEV'D?</span>
      {address ? (
        <span className="bg-white text-md rounded-full text-black py-2 px-4 border">
          {truncateAddress(address)}
        </span>
      ) : (
        <span className="text-md text-info py-2 px-4">Not connected</span>
      )}
    </div>
  );
}
