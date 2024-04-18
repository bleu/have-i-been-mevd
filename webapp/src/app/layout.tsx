import { RootLayout } from "#/components/RootLayout";
import { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: `MEV Scanner`,
  description: "Check how much funds you could have saved with MEV Blocker",
};

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-background flex h-full flex-col font-sans font-normal text-foreground border-foreground">
        <RootLayout>{children}</RootLayout>
      </body>
    </html>
  );
}
