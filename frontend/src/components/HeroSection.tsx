import { FaLocationArrow } from "react-icons/fa6";
import MagicButton from "./MagicButton";
import { TextGenerateEffect } from "./ui/TextGenerateEffect"; 





const HeroSection = ({
  title,
  mainText,
  subText,

  buttonTitle,
  buttonIcon,
  buttonPosition,
  buttonUrl,
  buttonClasses,
} :
{
  title: string;
  mainText: string;
  subText: string;

  buttonTitle: string;
  buttonIcon?: React.ReactNode;
  buttonPosition: string;
  buttonUrl: string;
  buttonClasses?: string;
}) => {
  return (
    <div className="relative pb-5 pt-12">

      {/**
       *  UI: grid
       *  change bg color to bg-black-100 and reduce grid color from
       *  0.2 to 0.03
       */}
      <div
        className="h-full w-auto bg-base-light dark:bg-base-dark bg-grid-base-dark/[0.03] bg-grid-base-dark-100/[0.2] 
           absolute top-0 left-0 flex items-center justify-center"
      >
        {/* Radial gradient for the container to give a faded look */}
        <div
          className="absolute pointer-events-none inset-0 flex items-center justify-center bg-base-light dark:bg-base-dark [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"
        />
      </div>

      <div className="flex justify-center relative my-20 z-10">
        <div className="max-w-[89vw] md:max-w-2xl lg:max-w-[60vw] flex flex-col items-center justify-center">
          <p className="uppercase tracking-widest text-xs text-center text-main-text-light dark:text-main-text-dark max-w-80">{ title }</p>

          {/**
           *  Link: https://ui.aceternity.com/components/text-generate-effect
           *
           *  change md:text-6xl, add more responsive code
           */}
          <TextGenerateEffect
            words={mainText}
            className="text-center text-[40px] md:text-5xl lg:text-6xl"
          />

          <p className="text-center md:tracking-wider mb-4 text-sm md:text-lg lg:text-2xl text-main-text-light dark:text-main-text-dark">{ subText }</p>

          <a href={buttonUrl}>
            <MagicButton
              title={buttonTitle}
              icon={buttonIcon}
              position={buttonPosition}
              otherClasses={buttonClasses}
            />
          </a>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;
