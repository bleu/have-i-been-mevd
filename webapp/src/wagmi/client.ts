import { getDefaultConfig, getDefaultWallets } from "@rainbow-me/rainbowkit";
import { http } from "wagmi";
import { mainnet } from "wagmi/chains";

/**
 * Project ID is required by Rainbowkit Migration Guide to Viem
 * 2. Supply a WalletConnect Cloud projectId
 * https://www.rainbowkit.com/docs/migration-guide#2-supply-a-walletconnect-cloud-projectid
 * Credentials for WalletConnect are available at 1Password
 */

const appName = "Have I Been Mev'd";
const projectId = "4f98524b2b9b5a80d14a519a8dcbecc2";
const chains = [mainnet] as const;

const { wallets } = getDefaultWallets({
  appName,
  projectId,
});

export const config = getDefaultConfig({
  appName,
  projectId,
  chains,
  transports: {
    [mainnet.id]: http(),
  },
  wallets,
});
