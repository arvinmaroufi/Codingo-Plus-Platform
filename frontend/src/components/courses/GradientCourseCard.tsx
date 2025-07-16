"use client";

import React from "react";
import { BackgroundGradient } from "../ui/BackgroundGradient";
import Course from "@/types/Course";

import Image from "next/image";
import Link from "next/link";

import { LuTimer } from 'react-icons/lu';
import { FaPlayCircle, FaUserTie, FaUserGraduate } from 'react-icons/fa';
import { RiSecurePaymentFill } from 'react-icons/ri';


export default function GradientCourseCard( data: Course) {
  console.log(data)

  return (
    <BackgroundGradient className="rounded-[22px] max-w-sm p-4 sm:p-10 bg-base-light dark:bg-base-dark">
      <Image
        src={data.poster}
        alt={data.title}
        height={400}
        width={400}
        className="object-contain rounded-2xl"
      />

      <div className="flex flex-col justify-between gap-6 items-start mt-5 mb-4">
        <p className="text-base sm:text-md text-main-text-light mt-2 dark:text-main-text-dark">{data.title}</p>
      </div>

      <hr />

      <div className="flex flex-row justify-between mt-3 mb-3">
        <span className="text-base sm:text-md text-primary-light dark:text-primary-dark p-3 rounded-xl">مقدماتی تا پیشرفته</span>
        <div className="flex flex-row justify-between items-center gap-1 p-2">
          <span className="text-base sm:text-md text-main-text-light dark:text-main-text-dark">
            {data.enrollment_count}
          </span>
          <FaUserGraduate className="mb-1 text-primary-light dark:text-primary-dark"/>
        </div>
      </div>

      <hr />

      <div className="flex flex-row justify-around gap-9 items-center mt-3 mb-3">
        <div className="flex flex-col justify-center items-start m-2">
          <div className="flex justify-evenly gap-2 text-base sm:text-md text-main-text-light mt-4 mb-2 dark:text-main-text-dark">
            <FaUserTie className="text-primary-dark dark:text-primary-light"/>
            <p>{data.teacher.full_name}</p>
          </div>

          <div className="flex justify-evenly gap-2 text-base sm:text-md text-main-text-light mt-4 mb-2 dark:text-main-text-dark">
            <LuTimer className="text-primary-dark dark:text-primary-light"/>
            <p>{data.duration}</p>
          </div>
        </div>
        <div className="flex flex-col justify-center items-start m-2 bg-success-light text-success-text-light border-success-text-dark dark:bg-success-dark dark:text-success-text-dark dark:border-success-light p-4 border-2 rounded-2xl">
          <p>40%</p>
          <p>تخفیف</p>
        </div>
      </div>

      <hr />

      <div className="flex flex-row justify-between items-center gap-5 mt-5">
        <div className="flex justify-evenly gap-2 text-base sm:text-md text-main-text-light mt-4 mb-2 dark:text-main-text-dark p-3 rounded-2xl">
          <del className="text-error-text-light dark:text-error-text-dark">{data.price}</del>
          <p className="text-success-text-light dark:text-success-text-dark">{data.price} تومان</p>
        </div>
        <div>
          <Link rel="stylesheet" href={`course/detail/${data.slug}`} className="flex justify-evenly gap-2 text-base sm:text-md text-main-text-light mt-4 mb-2 dark:text-main-text-dark bg-primary-light dark:bg-primary-dark p-3 rounded-2xl">
            <p>{data.is_enrolled ? 'یادگیری' : 'خرید'}</p>
            {data.is_enrolled === false && (
              <RiSecurePaymentFill className="text-primary-dark dark:text-primary-light mt-1"/>
            )}
            {data.is_enrolled === true && (
              <FaPlayCircle className="text-primary-dark dark:text-primary-light mt-1"/>
            )}
          </Link>
        </div>
      </div>

    </BackgroundGradient>
  );
}
