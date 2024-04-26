"use client";

import { Footer } from "#/components/Footer";
import { Header } from "#/components/Header";
import { Loading } from "#/components/Loading";
import { FreeMevReceipt, MevReceipt } from "#/components/Receipts";
import { getMevSummarized, IAddressMevData } from "#/utils/zeroMevApi";
import { useEffect, useState } from "react";
import { Address } from "viem";

export default function Page({
  params,
}: {
  params: {
    address: Address;
  };
}) {
  const [mevData, setMevData] = useState<IAddressMevData | undefined>();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (params.address) {
      getMevSummarized(params.address)
        .then(setMevData)
        .then(() => setLoading(false));
    }
  }, [params.address]);

  if (loading) {
    return (
      <div className="flex w-full justify-center h-full">
        <div className="flex flex-col items-center gap-8 justify-between w-1/2">
          <Header />
          <Loading />
          <Footer />
        </div>
      </div>
    );
  }

  return (
    <div className="flex w-full justify-center h-full">
      {mevData && mevData?.sum_user_loss_usd ? (
        <MevReceipt mevData={mevData} params={params} />
      ) : (
        <FreeMevReceipt address={params.address} />
      )}
    </div>
  );
}
