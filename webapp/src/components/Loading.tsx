import { useState, useEffect } from "react";
import Image from "next/image";

export function Loading() {
  const images = [
    "/assets/sandwiches/bread.svg",
    "/assets/sandwiches/cheese.svg",
    "/assets/sandwiches/ham.svg",
    "/assets/sandwiches/pickles.svg",
    "/assets/sandwiches/tomatoes.svg",
  ];

  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentImageIndex(
        (currentImageIndex) => (currentImageIndex + 1) % images.length
      );
    }, 500);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="flex flex-col md:flex-row w-full h-full justify-center items-center gap-8">
      <Image
        src={images[currentImageIndex]}
        alt="Loading..."
        height={100}
        width={100}
        objectFit="contain"
      />
      <span className="text-2xl">We’re preparing your order...</span>
    </div>
  );
}
