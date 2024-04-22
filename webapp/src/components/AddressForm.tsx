"use client";

import { useForm } from "react-hook-form";
import { Form, Button, InputField } from "@bleu-fi/ui";
import { scanAddressSchema } from "#/utils/schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useAccount } from "wagmi";
import { useEffect } from "react";

export function AddressForm() {
  const router = useRouter();
  const { address, isConnected } = useAccount();
  const form = useForm<typeof scanAddressSchema._type>({
    resolver: zodResolver(scanAddressSchema),
    reValidateMode: "onSubmit",
  });
  const { handleSubmit, setValue } = form;

  const onSubmit = async (data: typeof scanAddressSchema._type) => {
    router.push(`/mevreceipt/${data.address}`);
  };

  useEffect(() => {
    if (address && isConnected) {
      setValue("address", address);
    }
  }, [address]);

  return (
    <Form
      className="flex flex-col gap-4 w-full mt-3"
      {...form}
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit(onSubmit)();
      }}
    >
      <InputField
        // @ts-ignore
        form={form}
        field={{
          name: "address",
          label: "Address",
          mode: "text",
          type: "input",
          value: "",
        }}
      />
      <Button type="submit">Scan</Button>
    </Form>
  );
}
