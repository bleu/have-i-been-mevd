import { truncateAddress } from "#/utils/truncateAddress";
import { Address } from "viem";
import { CustomConnectButton } from "./CustomConnectButton";

export function Header({ address }: { address?: Address }) {
  return (
    <div className="flex flex-row w-full justify-between items-center border border-x-0 border-t-0 px-2 py-4">
      <span className="text-base md:text-xl font-bold">HAVE I BEEN MEV'D?</span>
      {address ? (
        <span className="bg-white text-md rounded-full text-black py-2 px-4 border">
          {truncateAddress(address)}
        </span>
      ) : (
        <CustomConnectButton />
      )}
    </div>
  );
}
