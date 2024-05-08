import { COLORS } from "#/utils/colors";
import { publicClient } from "#/utils/publicClient";
import { truncateAddress } from "#/utils/truncateAddress";
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
  runtime: "experimental-edge",
};

export const contentType = "image/png";

export default async function Image({
  params,
}: {
  params: {
    address: Address | string;
  };
}) {
  const addressToCheck = params.address.includes(".eth")
    ? await (publicClient.getEnsAddress({
        name: normalize(params.address),
      }) as Promise<Address>)
    : params.address;
  const mevData = await scanAddressMEV(addressToCheck as Address);
  const addressFormatted = params.address.includes(".eth")
    ? params.address
    : truncateAddress(params.address);

  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: `${COLORS.background}`,
          fontFamily: "var(--font-family-sans)",
        }}
      >
        <div tw="flex flex-col w-hull h-full justify-center items-center px-16 text-6xl">
          <div tw="flex md:flex-row flex-row w-full justify-between items-end">
            <span tw="font-bold">Hurrah!</span>
            <img
              src="http://localhost:3001/assets/share/mev_free_logo.svg"
              height={200}
              width={200}
            />
          </div>
          <div tw="flex text-5xl">
            <span tw="font-bold">{addressFormatted}</span>{" "}
            <span>is MEV-free</span>
          </div>
          <div
            tw={`w-full border border-t border-[${COLORS.border}] flex text-3xl w-full flex-row gap-2 justify-between`}
          >
            <span>@MEV_SCANNER</span>
          </div>
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
