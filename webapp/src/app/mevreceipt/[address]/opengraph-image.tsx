import { COLORS } from "#/utils/colors";
import { publicClient } from "#/utils/publicClient";
import { scanAddressMEV } from "#/utils/zeroMevApi";
import { ImageResponse } from "next/og";
import { Address } from "viem";
import { normalize } from "viem/ens";

export const alt = "About Acme";
export const size = {
  width: 1200,
  height: 630,
};

export const config = {
  runtime: "edge",
};

export const contentType = "image/png";

export default async function Image({
  params,
}: {
  params: {
    address: Address;
  };
}) {
  const addressToCheck = params.address.includes(".eth")
    ? await (publicClient.getEnsAddress({
        name: normalize(params.address),
      }) as Promise<Address>)
    : params.address;
  const mevData = await scanAddressMEV(addressToCheck as Address);

  return new ImageResponse(
    (
      <div
        style={{
          background: COLORS.background,
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "24px",
        }}
      >
        <div>
          <b>Hurrah!</b>
        </div>
        <span>This wallet is MEV-Free</span>
      </div>
    ),
    //   <div tw="flex flex-col bg-background items-left gap-8 justify-between w-full md:w-1/2 px-5">
    //     <div tw="flex flex-col justify-center gap-4">
    //       {/* <img src="/logo.svg" alt="Loading..." height={100} width={100} /> */}
    //       <span tw="text-2xl">Hurrah!</span>
    //       <span tw="text-5xl font-bold">This wallet is MEV-free</span>
    //       <div tw="flex flex-col gap-2 w-full">
    //         <h3 tw="text-xl">What is MEV?</h3>
    //         <div tw="text-wrap pl-4 border border-y-0 border-r-0">
    //           <p>
    //             MEV or “maximal extractable value” is a hidden tax on all types
    //             of Ethereum transactions
    //           </p>
    //           <br />
    //           <p>
    //             Anytime you make a DeFi trade, buy or sell an NFT, or lend
    //             tokens, opportunistic users known as “searchers” may manipulate
    //             your trades, resulting in unfavorable prices.
    //           </p>
    //         </div>
    //       </div>
    //     </div>
    //   </div>
    {
      ...size,
    }
  );
}
