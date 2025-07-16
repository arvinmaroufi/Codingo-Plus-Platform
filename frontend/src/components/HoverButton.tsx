import React from "react";

const HoverButton = ({
  title,
  icon,
  position,
  handleClick,
  otherClasses,
  is_active,
}: {
  title: string;
  icon?: React.ReactNode;
  position?: string;
  handleClick?: () => void;
  otherClasses?: string;
  is_active: boolean;
}) => {
  return (
    <button className={`${is_active ? 'bg-selected-light dark:bg-selected-dark text-sm font-bold text-main-text-dark dark:text-main-text-dark' : 'bg-base-light dark:bg-base-dark text-sm font-bold text-main-text-light dark:text-main-text-dark hover:bg-hover-light dark:hover:bg-hover-dark border-primary-light/[0.3] dark:border-primary-dark/[0.3]'} px-4 py-2 rounded-lg hover:-translate-y-1 transform transition duration-200 hover:shadow-md border-2`} onClick={handleClick}>
        <span
            className={`inline-flex h-full w-full cursor-pointer items-center justify-center font-bold backdrop-blur-3xl gap-3 ${otherClasses}`}
        >
            {position === "left" && icon}
            {title}
            {position === "right" && icon}
        </span>
    </button>
  );
};

export default HoverButton;