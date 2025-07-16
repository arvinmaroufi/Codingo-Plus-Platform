import { Fragment } from "react";

import { getServerSession } from "next-auth/next";

import { authOptions } from "@/app/api/auth/[...nextauth]/route";
import { MdOutlineFeaturedPlayList } from 'react-icons/md';

import CoursesFilter from "@/components/courses/CoursesFilter";
import HeroSection from "@/components/HeroSection";
import GradientCourseCard from "@/components/courses/GradientCourseCard";
import Course from "@/types/course"



export default async function CoursesPage() {

  const session = await getServerSession(authOptions);

  if (!session) {
    return <p className="text-center mt-20">Please sign in to view courses.</p>;
  }

  const jwt = session.accessToken as string;
  
  const response = await fetch(`${process.env.DJANGO_API_URL}courses/courses/`, {
    headers: { Authorization: `Bearer ${jwt}` },
    cache:"no-store",
  });

  const courses: Course[] = await response.json();

  return (
    <main className="flex justify-evenly items-center flex-col gap-12 overflow-hidden">
      <div className="max-w-7xl w-full">
        <HeroSection
          title="دوره هاس مجموعه"
          mainText="یادگیری برنامه نویسسی به سبک تفکر آن"
          subText="توسعه نرم افزار یک شغل نیستو یک سبک زندگی است"
          buttonTitle="ثبت نام در دوره های جدید"
          buttonIcon={ <MdOutlineFeaturedPlayList /> }
          buttonPosition="right"
          buttonUrl="/courses"
        />
      </div>
      <div className="grid grid-cols-12 items-start">
        <div className="flex justify-center items-center bg-base-light dark:bg-base-dark border-primary-light/[0.5] dark:border-primary-dark/[0.5] border-2 p-4 rounded-xl max-w-[20vw] xl:col-span-3 lg:col-span-3">
          <CoursesFilter />
        </div>
        <div className="grid gap-12 xl:grid-cols-3 lg:grid-cols-2 xl:col-span-9 lg:col-span-9">
          {courses.map(course => (
            <Fragment key={course.slug}>
              <GradientCourseCard {...course} />
            </Fragment>
          ))}
        </div>
      </div>
    </main>
  );
}
