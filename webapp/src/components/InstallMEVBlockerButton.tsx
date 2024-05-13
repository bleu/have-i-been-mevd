import { Button } from "@bleu-fi/ui";

export function InstallMEVBlockerButton() {
  return (
    <a
      target="_blank"
      rel="noopener noreferrer"
      href="https://mevblocker.io/#rpc"
      className="font-bold"
    >
      <Button className="rounded-full">Install MEV Blocker RPC</Button>
    </a>
  );
}
