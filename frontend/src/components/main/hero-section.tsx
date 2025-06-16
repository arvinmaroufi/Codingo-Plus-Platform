import { FaLocationArrow } from "react-icons/fa6";
import MagicButton from "../magic-button";
import { Spotlight } from "../ui/spotlight";
import { TextGenerateEffect } from "../ui/text-generate-effect";



const MainHeroSection = () => {
  return (
    <div className="relative pb-20 pt-36">
      {/**
       *  UI: Spotlights
       *  Link: https://ui.aceternity.com/components/spotlight
       */}
      <div>
        {/* Ensure the components use absolute positioning */}
        <Spotlight className="absolute -top-40 left-0 md:hidden" fill="white" />
        <Spotlight
          className="absolute h-[80vh] w-[50vw] top-10 left-full translate-x-[-100%]"
          fill="green"
        />
        <Spotlight
          className="absolute h-[80vh] w-[50vw] top-10 left-full translate-x-[-100%]"
          fill="green"
        />
        <Spotlight
          className="absolute h-[30vh] w-[30vw] top-[30px] left-[40px]"
          fill="green"
        />
        <Spotlight
          className="absolute h-[80vh] w-[50vw] top-[28px] left-[80px]"
          fill="blue"
        />
        <Spotlight
          className="absolute h-[80vh] w-[50vw] top-[12px] left-[11px]"
          fill="blue"
        />
        <Spotlight
          className="absolute h-[80vh] w-[50vw] top-[19px] left-[30px]"
          fill="blue"
        />
      </div>

      {/**
       *  UI: grid
       *  change bg color to bg-black-100 and reduce grid color from
       *  0.2 to 0.03
       */}
      <div
        className="h-screen w-full bg-base-light dark:bg-base-dark bg-grid-base-dark/[0.03] bg-grid-base-dark-100/[0.2] 
           absolute top-0 left-0 flex items-center justify-center"
      >
        {/* Radial gradient for the container to give a faded look */}
        <div
          className="absolute pointer-events-none inset-0 flex items-center justify-center bg-base-light dark:bg-base-dark [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"
        />
      </div>

      <div className="flex justify-center relative my-20 z-10">
        <div className="max-w-[89vw] md:max-w-2xl lg:max-w-[60vw] flex flex-col items-center justify-center">
          <p className="uppercase tracking-widest text-xs text-center text-main-text-light dark:text-main-text-dark max-w-80">
            کدینگو پلاس
          </p>

          {/**
           *  Link: https://ui.aceternity.com/components/text-generate-effect
           *
           *  change md:text-6xl, add more responsive code
           */}
          <TextGenerateEffect
            words="آموزش توسعه و مهندسی نرم افزار"
            className="text-center text-[40px] md:text-5xl lg:text-6xl"
          />

          <p className="text-center md:tracking-wider mb-4 text-sm md:text-lg lg:text-2xl text-main-text-light dark:text-main-text-dark">
            به مجموعه ی کدینگو خوش آمدید
          </p>

          <a href="#about">
            <MagicButton
              title="مشاهده ی دوره ها"
              icon={<FaLocationArrow />}
              position="right"
            />
          </a>
        </div>
      </div>
    </div>
  );
};

export default MainHeroSection;
