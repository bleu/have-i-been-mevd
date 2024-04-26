import Image from "next/image";
import { Address } from "viem";
import { Header } from "./Header";
import { Footer } from "./Footer";
import { APP_URL, TwitterShareButton } from "./TwitterShareButton";
import { TradeOnCoWButton } from "./TradeOnCoWButton";
import { BackToHomeButton } from "./BackToHomeButton";

export function FreeMevReceipt({ address }: { address?: Address }) {
  const twitterShareText = `I found out that the address ${address} is MEV-free. Check if your address lost money to MEV bots at ${APP_URL}`;

  return (
    <div className="flex flex-col items-left gap-8 justify-between w-1/2">
      <Header address={address} />
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
