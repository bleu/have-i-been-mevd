"use client";

import Image from "next/image";
import { useForm } from "react-hook-form";
import { Form, Button, InputField } from "@bleu-fi/ui";
import { scanAddressSchema } from "#/utils/schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { CustomConnectButton } from "./CustomConnectButton";
import { ArrowRightIcon } from "@radix-ui/react-icons";

export function AddressForm() {
  const router = useRouter();
  const form = useForm<typeof scanAddressSchema._type>({
    resolver: zodResolver(scanAddressSchema),
    reValidateMode: "onSubmit",
  });
  const { handleSubmit } = form;

  const onSubmit = async (data: typeof scanAddressSchema._type) => {
    router.push(`/mevreceipt/${data.address}`);
  };

  return (
    <div className="flex flex-col justify-center h-full w-full gap-8 mb-32">
      <Form
        className="flex flex-col gap-4 w-full justify-center"
        {...form}
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit(onSubmit)();
        }}
      >
        <div className="flex flex-row gap-2 justify-between items-end">
          <p className="text-2xl text">
            Wanna know if you’ve left crumbs <br /> on the table?
          </p>
          <Image src={"/assets/crumbs.svg"} height={200} width={200} alt="" />
        </div>
        <div className="flex flex-row justify-between items-end gap-2">
          <InputField
            // @ts-ignore
            form={form}
            field={{
              name: "address",
              placeholder: "Enter an Ethereum or an ENS address",
              mode: "text",
              type: "input",
              value: "",
            }}
          />
          <Button
            type="submit"
            variant="ghost"
            className="rounded-full border px-3 py-5"
          >
            <ArrowRightIcon className="size-5" />
          </Button>
        </div>
      </Form>
      <div className="flex flex-row gap-2 items-center">
        <span>or</span>
        <CustomConnectButton />
      </div>
    </div>
  );
}
