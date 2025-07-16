import { Fragment } from "react";

import { getServerSession } from "next-auth/next";

import GradientCourseCard from "@/components/courses/GradientCourseCard";

import { authOptions } from "@/app/api/auth/[...nextauth]/route";

import Course from "@/types/Course";

import HeroSection from "@/components/HeroSection";
import { MdOutlineFeaturedPlayList } from 'react-icons/md';




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
    <main className="relative bg-black-100 flex justify-center items-center flex-col overflow-hidden mx-auto sm:px-10 px-5">
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
      <div className="grid gap-12 lg:grid-cols-3 md:grid-cols-2 grid-cols-1">
        {courses.map(course => (
          <Fragment key={course.slug}>
            <GradientCourseCard {...course} />
          </Fragment>
        ))}
      </div>
    </main>
  );
}
