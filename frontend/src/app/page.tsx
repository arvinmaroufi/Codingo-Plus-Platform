import MainHeroSection from "@/components/main/hero-section";

export default function Home() {
  return (
    <main className="relative bg-black-100 flex justify-center items-center flex-col overflow-hidden mx-auto sm:px-10 px-5">
      <div className="max-w-7xl w-full">
        <MainHeroSection />
      </div>
    </main>
  );
}
