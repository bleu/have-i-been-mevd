import { normalize } from "viem/ens";
import { isAddress } from "viem";

import { z } from "zod";
import { publicClient } from "./publicClient";

const basicAddressSchema = z.string().refine((value) => isAddress(value), {
  message: "Provided address is invalid",
});

const ensAddressSchema = z.string().refine(
  async (value) => {
    if (!value.includes(".eth")) {
      return false;
    }
    try {
      const address = await publicClient.getEnsAddress({
        name: normalize(value),
      });
      return address !== null;
    } catch {
      return false;
    }
  },
  {
    message: "Provided address is invalid",
  }
);

export const scanAddressSchema = z.object({
  address: z.union([basicAddressSchema, ensAddressSchema]),
});
