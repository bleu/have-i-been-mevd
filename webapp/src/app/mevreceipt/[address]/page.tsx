"use client";

import { Spinner } from "#/components/Spinner";
import { TwitterShareButton } from "#/components/TwitterShareButton";
import { truncateAddress } from "#/utils/truncateAddress";
import { IAddressMevData, scanAddressMEV } from "#/utils/zeroMevApi";
import { Button, capitalize, formatNumber } from "@bleu-fi/ui";
import { HomeIcon, TwitterLogoIcon } from "@radix-ui/react-icons";
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

  const totalAmountUsdFormatted = `$ ${formatNumber(mevData.totalAmountUsd)}`;

  const protocolNameFormatted = `${capitalize(mevData.mostMevProtocolName)}`;

  const mostMevProtocolUsdAmountFormatted = `$ ${formatNumber(
    mevData.mostMevProtocolUsdAmount
  )}`;

  const twitterShareText = `I found out that I have received ${totalAmountUsdFormatted} on ${mevData.mevTxsLength} transactions. Most MEV from ${protocolNameFormatted} (${mostMevProtocolUsdAmountFormatted}).\n\nStop feeding the MEV bots. Install MEV Blocker: https://mevblocker.io\n\n`;

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
            <b className="text-highlight">{totalAmountUsdFormatted}</b> (on{" "}
            {mevData.mevTxsLength} transactions)
          </div>
          <div>
            Most MEV from:{" "}
            <i className="text-accent">{protocolNameFormatted}</i> (
            {mostMevProtocolUsdAmountFormatted})
          </div>
          <div className="flex flex-row w-full justify-between gap-5 text-xl">
            <Link href="/" className="w-full">
              <Button
                type="button"
                className="w-full flex items-center gap-3 justify-self-start py-5"
              >
                <HomeIcon className="size-6" /> Scan another address
              </Button>
            </Link>
            <TwitterShareButton
              type="button"
              className="w-full flex items-center gap-3 justify-self-start py-5"
              text={twitterShareText}
            >
              <TwitterLogoIcon className="size-6" /> Share
            </TwitterShareButton>
          </div>
        </div>
      </div>
    </div>
  );
}
