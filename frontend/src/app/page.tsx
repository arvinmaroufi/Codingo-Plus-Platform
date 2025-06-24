import { BsCollectionPlay } from "react-icons/bs";


import HeroSection from "@/components/HeroSection";



export default function Home() {
  return (
    <main className="relative bg-black-100 flex justify-center items-center flex-col overflow-hidden mx-auto sm:px-10 px-5">
      <div className="max-w-7xl w-full">
        <HeroSection
          title="مجموعه ی کدینگو"
          mainText="آموزش توسعه و مهندسی نرم افزار"
          subText="به مجموعه ی کدینگو خوش آمدید"

          buttonTitle="مشاهده ی دوره ها"
          buttonIcon={ <BsCollectionPlay /> }
          buttonPosition="right"
          buttonUrl="/courses"
        />
      </div>
    </main>
  );
}
