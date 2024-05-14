"use client";

import { AddressForm } from "#/components/AddressForm";
import { Footer } from "#/components/Footer";
import { Header } from "#/components/Header";
import { useAccountEffect } from "#/wagmi";
import { useRouter } from "next/navigation";
import { publicClient } from "#/utils/publicClient";
import { Address } from "viem";
import { useEffect } from "react";

export default function Page() {
  async function pushToReceipt(address?: Address) {
    if (address) {
      const ensName = await publicClient.getEnsName({ address });
      const receiptString = ensName ? ensName : address;
      router.push(`/mevreceipt/${receiptString}`);
    }
  }
  const router = useRouter();
  useAccountEffect({
    onConnect(data) {
      pushToReceipt(data.address);
    },
  });

  useEffect;

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
