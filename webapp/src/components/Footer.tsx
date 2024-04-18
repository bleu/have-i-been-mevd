export function Footer() {
  return (
    <footer className="flex w-full justify-between p-4 text-foreground/90 text-sm">
      <span>
        developed by&nbsp;
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/bleu-fi"
          className="font-bold text-primary"
        >
          bleu
        </a>
      </span>
      <div className="float-right flex flex-row items-center space-x-4">
        <div>
          powered by &nbsp;
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://zeromev.org/"
            className="font-bold text-accent"
          >
            zeromev
          </a>
        </div>
      </div>
    </footer>
  );
}
