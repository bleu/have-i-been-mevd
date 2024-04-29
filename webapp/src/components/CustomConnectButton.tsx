import { ConnectButton } from "@rainbow-me/rainbowkit";

import { Button } from "@bleu-fi/ui";
import { truncateAddress } from "#/utils/truncateAddress";

export function CustomConnectButton() {
  return (
    <ConnectButton.Custom>
      {({
        account,
        chain,
        openAccountModal,
        openConnectModal,
        authenticationStatus,
        mounted,
      }) => {
        const ready = mounted && authenticationStatus !== "loading";
        const connected = ready && account && chain;
        return (
          <div
            {...(!ready && {
              "aria-hidden": true,
              className: "opacity-0 pointer-events-none select-none",
            })}
          >
            {(() => {
              if (!connected) {
                return (
                  <>
                    <Button
                      onClick={openConnectModal}
                      shade="dark"
                      className="rounded-full"
                    >
                      Connect your wallet
                    </Button>
                  </>
                );
              }
              return (
                <Button
                  onClick={openAccountModal}
                  shade="dark"
                  className="rounded-full"
                >
                  {truncateAddress(account.address)}
                </Button>
              );
            })()}
          </div>
        );
      }}
    </ConnectButton.Custom>
  );
}
