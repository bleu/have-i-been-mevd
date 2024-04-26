export function Footer() {
  return (
    <footer className="flex w-full justify-between text-foreground/90 text-md py-4 border-t-2">
      <span>
        developed by&nbsp;
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/bleu-fi"
          className="font-bold text-sky-600"
        >
          bleu
        </a>
        &nbsp;using data from&nbsp;
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://zeromev.org/"
          className="font-bold"
        >
          zeromev
        </a>
      </span>
      <div className="float-right flex flex-row items-center space-x-4">
        <div>
          Visit&nbsp;
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://cow.fi/"
            className="font-bold underline underline-offset-4"
          >
            CoW Swap
          </a>
        </div>
      </div>
    </footer>
  );
}
