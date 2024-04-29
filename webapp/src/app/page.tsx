"use client";

import { AddressForm } from "#/components/AddressForm";
import { Footer } from "#/components/Footer";
import { Header } from "#/components/Header";
import { useAccount } from "#/wagmi";
import { config } from "#/wagmi/client";
import { disconnect } from "@wagmi/core";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Page() {
  const { address, isConnected } = useAccount();

  const router = useRouter();

  useEffect(() => {
    if (address && isConnected) {
      router.push(`/mevreceipt/${address}`);
    }
  }, [address]);

  useEffect(() => {
    disconnect(config);
  });

  return (
    <div className="flex w-full justify-center h-full">
      <div className="flex flex-col items-center gap-8 justify-between w-1/2">
        <Header />
        <AddressForm />
        <Footer />
      </div>
    </div>
  );
}
