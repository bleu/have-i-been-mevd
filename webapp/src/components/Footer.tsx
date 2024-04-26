export function Footer() {
  return (
    <footer className="flex w-full justify-between text-md py-4 border border-x-0 border-b-0">
      <span>
        developed by&nbsp;
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/bleu-fi"
          className="font-extrabold"
        >
          bleu
        </a>
        &nbsp;using&nbsp;
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://zeromev.org/"
          className="font-extrabold"
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
            className="font-extrabold underline underline-offset-4"
          >
            CoW Swap
          </a>
        </div>
      </div>
    </footer>
  );
}
