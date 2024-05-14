import { Button, ButtonProps } from "@bleu-fi/ui";

export interface TwitterShareButtonProps extends Omit<ButtonProps, "onClick"> {
  text: string;
}

export const APP_URL = "https://have-i-been-mevd.bleu.fi/";

export function TwitterShareButton({ text }: TwitterShareButtonProps) {
  const shareUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`;

  const handleShare = (e: { preventDefault: () => void }) => {
    e.preventDefault();
    window.open(shareUrl, "twitter-share", "width=550,height=235");
  };

  return (
    <Button
      onClick={handleShare}
      variant="ghost"
      className="border rounded-full hover:text-foreground"
    >
      Share
    </Button>
  );
}
