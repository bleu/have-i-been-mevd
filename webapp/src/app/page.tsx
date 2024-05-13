"use client";

import { AddressForm } from "#/components/AddressForm";
import { Footer } from "#/components/Footer";
import { Header } from "#/components/Header";
import { useAccount } from "#/wagmi";
import { config } from "#/wagmi/client";
import { disconnect } from "@wagmi/core";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { publicClient } from "#/utils/publicClient";
import { Address } from "viem";

export default function Page() {
  const { address, isConnected } = useAccount();

  const router = useRouter();

  async function pushToReceipt(address?: Address, isConnected?: boolean) {
    if (address && isConnected) {
      const ensName = await publicClient.getEnsName({ address });
      const receiptString = ensName ? ensName : address;
      router.push(`/mevreceipt/${receiptString}`);
    }
  }

  useEffect(() => {
    pushToReceipt(address, isConnected);
  }, [address]);

  useEffect(() => {
    disconnect(config);
  });

  return (
    <div className="flex w-full justify-center h-full">
      <div className="flex flex-col items-center gap-8 justify-between w-full md:w-1/2">
        <Header />
        <AddressForm />
        <Footer />
      </div>
    </div>
  );
}
