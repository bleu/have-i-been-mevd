import { Button, ButtonProps } from "@bleu-fi/ui";

export interface TwitterShareButtonProps extends Omit<ButtonProps, "onClick"> {
  text: string;
}

const APP_URL = "https://have-i-been-meved.vercel.app/";

export function TwitterShareButton({
  text,
  children,
  ...props
}: TwitterShareButtonProps) {
  const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(APP_URL)}&text=${encodeURIComponent(text)}`;

  const handleShare = (e: { preventDefault: () => void }) => {
    e.preventDefault();
    window.open(shareUrl, "twitter-share", "width=550,height=235");
  };

  return (
    <Button onClick={handleShare} {...props}>
      {children}
    </Button>
  );
}
