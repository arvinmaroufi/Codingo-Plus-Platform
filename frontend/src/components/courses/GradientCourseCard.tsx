"use client";

import React from "react";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { LuTimer } from 'react-icons/lu';
import { FaPlayCircle, FaUserTie, FaUserGraduate } from 'react-icons/fa';
import { RiSecurePaymentFill } from 'react-icons/ri';

import Course from "@/types/course";

import { BackgroundGradient } from "../ui/BackgroundGradient";
import HoverButton from "../HoverButton";



export default function GradientCourseCard( data: Course) {

  const router = useRouter()

  const tolggleDetailPage= () => {
    router.push(`/courses/${data.slug}`)
  }

  return (
    <div className="w-full">
      <BackgroundGradient className="rounded-[22px] max-w-sm p-4 sm:p-10 bg-base-light dark:bg-base-dark flex flex-col justify-evenly gap-3">
        <Image
          src={data.poster}
          alt={data.title}
          height={400}
          width={400}
          className="object-contain rounded-2xl"
        />

        <div className="flex items-center justify-center">
          <p className="text-base sm:text-md text-main-text-light mt-2 dark:text-main-text-dark">{data.title}</p>
        </div>

        <div className="flex justify-between border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
          <span className="text-base sm:text-md text-primary-light dark:text-primary-dark rounded-xl mt-3 mb-3">مقدماتی تا پیشرفته</span>
          <div className="flex justify-between items-center gap-1 mt-3 mb-3">
            <span className="text-base sm:text-md text-main-text-light dark:text-main-text-dark">
              {data.enrollment_count}
            </span>
            <FaUserGraduate className="mb-1 text-primary-light dark:text-primary-dark"/>
          </div>
        </div>

        <div className="flex justify-around gap-9 items-center border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
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

        <div className="flex justify-between items-center border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
          <div className="flex justify-evenly gap-2 text-base sm:text-md text-main-text-light mt-6 dark:text-main-text-dark rounded-2xl">
            <del className="text-error-text-light dark:text-error-text-dark">{data.price}</del>
            <p className="text-success-text-light dark:text-success-text-dark">{data.price} تومان</p>
          </div>
          <div className="mt-6">
            <HoverButton
              title={data.is_enrolled ? 'یادگیری' : 'خرید'}
              is_active={data.is_enrolled}
              icon={data.is_enrolled ? <FaPlayCircle /> : <RiSecurePaymentFill />}
              position="right"
              handleClick={tolggleDetailPage}
            />
          </div>
        </div>
      </BackgroundGradient>
    </div>
    
  );
}
