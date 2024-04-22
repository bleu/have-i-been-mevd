"use client";

import { AddressForm } from "#/components/AddressForm";
import { CustomConnectButton } from "#/components/CustomConnectButton";

export default function Page() {
  return (
    <div className="flex w-full justify-center h-full">
      <div className="flex flex-col items-center gap-8 justify-center">
        <h1 className="text-6xl">MEV Scanner</h1>
        <AddressForm />
        <p className="text-lg">or</p>
        <CustomConnectButton />
      </div>
    </div>
  );
}
