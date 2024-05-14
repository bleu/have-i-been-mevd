"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import { Toaster } from "@bleu-fi/ui";
import React from "react";
import Fonts from "./Fonts";
import merge from "lodash.merge";

import { WagmiProvider } from "wagmi";
import { config } from "#/wagmi/client";
import { RainbowKitProvider, Theme, darkTheme } from "@rainbow-me/rainbowkit";
import { mainnet } from "viem/chains";
import { COLORS } from "#/utils/colors";

export function RootLayout({ children }: React.PropsWithChildren) {
  const queryClient = new QueryClient();

  return (
    <>
      <WagmiProvider config={config} reconnectOnMount={false}>
        <QueryClientProvider client={queryClient}>
          <RainbowKitProvider
            initialChain={mainnet}
            modalSize="compact"
            theme={CustomTheme}
          >
            <Fonts />
            <div className="flex flex-col h-screen">{children}</div>
            <Toaster />
          </RainbowKitProvider>
        </QueryClientProvider>
      </WagmiProvider>
    </>
  );
}

const CustomTheme = merge(darkTheme(), {
  colors: {
    accentColor: COLORS.foreground,
    accentColorForeground: COLORS["accent-foreground"],
    closeButtonBackground: COLORS.background,
    closeButton: COLORS.foreground,
    connectButtonTextError: COLORS.destructive,
    generalBorder: COLORS.border,
    modalBackground: COLORS.background,
    modalBorder: COLORS.border,
    modalText: COLORS.foreground,
    modalTextSecondary: COLORS.foreground,
    selectedOptionBorder: COLORS.border,
  },
  fonts: {
    body: "var(--font-family-sans)",
  },
  radii: {
    menuButton: "25px",
    modal: "25px",
  },
} as Theme);
