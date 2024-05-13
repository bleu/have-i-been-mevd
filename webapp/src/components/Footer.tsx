export function Footer() {
  return (
    <footer className="flex w-full justify-between text-xs md:text-sm px-2 py-4 border border-x-0 border-b-0">
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
        &nbsp;and funded by the&nbsp;
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://cow.fi/"
          className="font-extrabold"
        >
          CoW DAO Grants Program
        </a>
      </span>
    </footer>
  );
}
