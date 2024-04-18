"use client";

import { Toaster } from "@bleu-fi/ui";
import React from "react";
import Fonts from "./Fonts";
import { Footer } from "./Footer";

export function RootLayout({ children }: React.PropsWithChildren) {
  return (
    <>
      <Fonts />
      <div className="flex flex-col h-screen">
        <div className="size-full">{children}</div>
        <Footer />
      </div>
      <Toaster />
    </>
  );
}
