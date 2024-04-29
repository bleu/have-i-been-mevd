import Image from "next/image";
import { Address } from "viem";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { APP_URL, TwitterShareButton } from "./TwitterShareButton";
import { TradeOnCoWButton } from "./TradeOnCoWButton";
import { BackToHomeButton } from "./BackToHomeButton";
import { IAddressMevData } from "#/utils/zeroMevApi";
import { formatNumber } from "@bleu-fi/ui";

export function FreeMevReceipt({
  addressBytes,
  addressName,
}: {
  addressBytes: Address;
  addressName: string;
}) {
  const twitterShareText = `I found out that the address ${addressName} is MEV-free. Check if your address lost money to MEV bots at ${APP_URL}`;

  return (
    <div className="flex flex-col items-left gap-8 justify-between w-full md:w-1/2 px-5">
      <Header address={addressBytes} />
      <div className="flex flex-col justify-center gap-4">
        <Image
          src="/logo.svg"
          alt="Loading..."
          height={100}
          width={100}
          objectFit="contain"
        />
        <span className="text-2xl">Hurrah!</span>
        <span className="text-5xl font-bold">This wallet is MEV-free</span>
        <div className="flex flex-col gap-2 w-full">
          <h3 className="text-xl">What is MEV?</h3>
          <div className="text-wrap pl-4 border border-y-0 border-r-0">
            <p>
              MEV or “maximal extractable value” is a hidden tax on all types of
              Ethereum transactions
            </p>
            <br />
            <p>
              Anytime you make a DeFi trade, buy or sell an NFT, or lend tokens,
              opportunistic users known as “searchers” may manipulate your
              trades, resulting in unfavorable prices.
            </p>
          </div>
        </div>
        <div className="flex flex-row gap-2">
          <BackToHomeButton />
          <TwitterShareButton text={twitterShareText} />
          <TradeOnCoWButton />
        </div>
      </div>
      <Footer />
    </div>
  );
}

export function MevReceipt({
  mevData,
  addressBytes,
  addressName,
}: {
  mevData: IAddressMevData;
  addressBytes: Address;
  addressName: string;
}) {
  const totalAmountUsdFormatted = `$${((mevData?.sum_user_loss_usd || 0) * -1).toFixed()}`;
  const totalVolumeUsdFormatted = `$${formatNumber(mevData?.sum_user_swap_volume_usd || 0)}`;

  const twitterShareText = `I found out that this wallet ${addressName} is toasted, it lost ${totalAmountUsdFormatted} on ${mevData?.sum_user_swap_count || 0} MEV transactions. Install MEV Blocker: https://mevblocker.io\n\nScan your wallet using ${APP_URL}`;

  return (
    <div className="bg-primary py-16 w-full h-full">
      <div className="flex flex-col h-full w-full items-center justify-between bg-gradient-diagonal-to-tr from-destructive-light to-destructive to-50% text-background">
        <div className="top-sandwich-background h-2/5 " />
        <div className="flex flex-col items-left h-full justify-between w-full md:w-1/2 px-5 gap-8">
          <Header address={addressBytes} />
          <div className="flex flex-col gap-2 text-primary">
            <span className="text-3xl">This wallet is toast!</span>
            <span className="text-background font-extrabold text-6xl">
              {totalAmountUsdFormatted} eaten away
            </span>
            <span className="text-3xl font-semibold">
              in{" "}
              <span className="font-bold">
                {mevData?.sum_user_swap_count} transactions{" "}
              </span>
              for a{" "}
              <span className="font-bold">
                volume of {totalVolumeUsdFormatted}
              </span>
            </span>
            <div className="flex flex-col justify-center gap-4 text-background">
              <div className="flex flex-row gap-2">
                <BackToHomeButton />
                <TwitterShareButton text={twitterShareText} />
                <TradeOnCoWButton />
              </div>
            </div>
          </div>
          <Footer />
        </div>
        <div className="bottom-sandwich-background h-2/5" />
      </div>
    </div>
  );
}
