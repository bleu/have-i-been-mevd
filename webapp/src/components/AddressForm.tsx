"use client";

import { useForm } from "react-hook-form";
import { Form, Button, InputField } from "@bleu-fi/ui";
import { scanAddressSchema } from "#/utils/schema";
import { zodResolver } from "@hookform/resolvers/zod";

export function AddressForm() {
  const form = useForm<typeof scanAddressSchema._type>({
    resolver: zodResolver(scanAddressSchema),
    reValidateMode: "onSubmit",
  });
  const { handleSubmit } = form;

  return (
    <Form
      className="flex flex-col gap-4 w-full mt-3"
      {...form}
      onSubmit={(e) => {
        e.preventDefault();
        handleSubmit((data) => {
          console.log(data);
        })();
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
