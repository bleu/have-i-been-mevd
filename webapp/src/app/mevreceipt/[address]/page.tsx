"use client";

import { Spinner } from "#/components/Spinner";
import { truncateAddress } from "#/utils/truncateAddress";
import { IAddressMevData, scanAddressMEV } from "#/utils/zeroMevApi";
import { Button, capitalize, formatNumber } from "@bleu-fi/ui";
import { HomeIcon } from "@radix-ui/react-icons";
import Link from "next/link";
import { useEffect, useState } from "react";
import { Address } from "viem";

export default function Page({
  params,
}: {
  params: {
    address: Address;
  };
}) {
  const [mevData, setMevData] = useState<IAddressMevData | null>(null);

  useEffect(() => {
    if (params.address) {
      scanAddressMEV(params.address).then(setMevData);
    }
  }, [params.address]);

  if (!mevData) {
    return (
      <div className="flex w-full justify-center h-full">
        <div className="flex flex-col items-center gap-8 justify-center">
          <Spinner />
        </div>
      </div>
    );
  }

  return (
    <div className="flex w-full justify-center h-full">
      <div className="flex flex-col items-center gap-8 justify-center">
        <h1 className="text-5xl">
          MEV Receipt for{" "}
          <b className="text-highlight">{truncateAddress(params.address)}</b>
        </h1>
        <div className="flex flex-col gap-4 text-2xl">
          <div>
            Total amount:{" "}
            <b className="text-highlight">
              ${formatNumber(mevData.totalAmountUsd)} USD
            </b>{" "}
            (on {mevData.mevTxsLength} transactions)
          </div>
          <div>
            Most MEV from:{" "}
            <i className="text-accent">
              {capitalize(mevData.mostMevProtocolName)}
            </i>{" "}
            ($
            {formatNumber(mevData.mostMevProtocolUsdAmount)} USD)
          </div>
          <Link href="/" className="w-full">
            <Button
              type="button"
              className="w-full flex items-center gap-3 justify-self-start text-xl py-5"
            >
              <HomeIcon className="size-6" /> Scan another address
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
