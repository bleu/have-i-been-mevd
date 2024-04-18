import { isAddress } from "viem";
import { z } from "zod";

const basicAddressSchema = z
  .string()
  .length(42)
  .refine((value) => isAddress(value), {
    message: "Provided address is invalid",
  });

export const scanAddressSchema = z.object({
  address: basicAddressSchema,
});
