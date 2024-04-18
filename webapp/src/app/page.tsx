import { AddressForm } from "#/components/AddressForm";

export default function Home() {
  return (
    <div className="flex w-full justify-center h-full">
      <div className="flex flex-col items-center gap-8 justify-center">
        <h1 className="text-6xl">MEV Scanner</h1>
        <AddressForm />
      </div>
    </div>
  );
}
