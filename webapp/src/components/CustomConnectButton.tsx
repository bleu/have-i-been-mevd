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
        console.log(account);
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
                    <Button onClick={openConnectModal} shade="dark">
                      Connect Wallet
                    </Button>
                  </>
                );
              }
              return (
                <Button onClick={openAccountModal} shade="dark">
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
