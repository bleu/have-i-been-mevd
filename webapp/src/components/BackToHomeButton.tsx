import { useDisconnect } from "#/wagmi";
import { Button } from "@bleu-fi/ui";
import { ArrowLeftIcon } from "@radix-ui/react-icons";
import { useRouter } from "next/navigation";

export function BackToHomeButton() {
  const { disconnect } = useDisconnect();
  const router = useRouter();

  const onClick = () => {
    disconnect();
    router.push("/");
  };

  return (
    <Button
      onClick={onClick}
      variant="ghost"
      className="rounded-full border py-0 px-2 hover:text-foreground"
    >
      <ArrowLeftIcon className="size-5" />
    </Button>
  );
}
