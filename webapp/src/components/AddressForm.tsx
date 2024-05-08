"use client";

import { useForm } from "react-hook-form";
import { Form, Button, InputField } from "@bleu-fi/ui";
import { scanAddressSchema } from "#/utils/schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
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
    <div className="flex flex-col justify-center h-full w-full gap-8 mb-32 px-5">
      <Form
        className="flex flex-col gap-4 w-full justify-center"
        {...form}
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit(onSubmit)();
        }}
      >
        <div className="flex flex-row gap-2 justify-between items-end w-full">
          <p className="text-2xl md:text-4xl text-wrap w-3/5">
            Wanna know if you’ve left crumbs on the table?
          </p>
          <img src={"/assets/crumbs.svg"} className="max-w-none" alt="" />
        </div>
        <div className="flex flex-row justify-between items-start gap-2">
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
            style={{ display: "none" }}
          />
          <div className="space-y-2">
            <p className="text-muted-foreground text-sm" />
            <Button
              type="submit"
              variant="ghost"
              className="rounded-full border px-2 py-5"
            >
              <ArrowRightIcon className="size-5" />
            </Button>
          </div>
        </div>
      </Form>
    </div>
  );
}
