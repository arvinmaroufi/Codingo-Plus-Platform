'use client';

import { useReducer, useState, useEffect } from 'react';

import Image from 'next/image';

import { FaAngleDown } from "react-icons/fa";

import { Input } from '../ui/Input';
import { Label } from '../ui/label';
import HoverButton from '../HoverButton';

import SubCategory from '@/types/sub-category';

import { courseFiltersData } from '@/data';




interface Categories {
  slug: string;
  title: string;
  icon: string;
  created_at: string;
  updated_at: string
  sub_categories: SubCategory[];
}



export default function CoursesFilter() {

  const [ categories, SetCategories ] = useState<Categories[]>([]);

  // Filters states
  const [ courseStatus, setCourseStatus ] = useState(courseFiltersData.courseStatus);
  const [ levelStatus, setLevelStatus ] = useState(courseFiltersData.levelStatus);
  const [ paymentStatus, setPaymentStatus ] = useState(courseFiltersData.paymentStatus);
  const [ languageStatus, setLanguageStatus ] = useState(courseFiltersData.languageStatus);
  const [ ordering, setOrdering ] = useState(courseFiltersData.ordering);


  const setCourseStatusFilter = (id: number) => {
    setCourseStatus(prev =>
      prev.map(item => ({
        ...item,
        // if it’s the clicked one, flip its current flag,
        // otherwise always turn others off
        is_active: item.id === id ? !item.is_active : false
      }))
    );
  };

  const setLevelStatusFilter = (id: number) => {
    setLevelStatus(prev =>
      prev.map(item => ({
        ...item,
        // if it’s the clicked one, flip its current flag,
        // otherwise always turn others off
        is_active: item.id === id ? !item.is_active : false
      }))
    );
  };

  const setPaymentStatusFilter = (id: number) => {
    setPaymentStatus(prev =>
      prev.map(item => ({
        ...item,
        // if it’s the clicked one, flip its current flag,
        // otherwise always turn others off
        is_active: item.id === id ? !item.is_active : false
      }))
    );
  };

  
  useEffect(() => {
    async function fetchCategories() {
      const res = await fetch(`${process.env.DJANGO_API_URL}courses/categories/`)
      const fetchedData: Categories[] = await res.json()
      SetCategories(fetchedData);
    }
    fetchCategories();
  }, []);

  return (
    <div className="flex flex-col justify-evenly gap-3">
      <h3 className="text-2xl font-bold text-center text-main-text-light dark:text-main-text-dark p-2">فیلتر</h3>

      {/* search */}
      <form className="flex flex-col justify-between gap-2 p-3">
          <Label htmlFor="search" className="text-md font-bold">جستوجوی دوره</Label>
          <Input id="search" type="text" className="text-md font-bold"/>
      </form>

      <div className="flex flex-col justify-evenly gap-3 pt-3 border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
        <h4 className="text-lg font-bold text-center text-main-text-light dark:text-main-text-dark p-2">دسته بندی ها</h4>
        <div className="flex flex-col justify-evenly gap-3">

          <div className="flex flex-col justify-between gap-2">
            <Input id="search" type="text" className="text-md font-bold" placeholder='جستوجو'/>
          </div>

          <div className="flex flex-col justify-between gap-4 p-2">
            <h5 className="text-md font-bold text-start text-main-text-light dark:text-main-text-dark pr-2">لیست دسته بندی</h5>
            <div className="flex flex-col justify-evenly gap-2">
              {categories.map((item) => (
                <CategoriesList key={item.slug} item={item}/>
              ))}
            </div>
          </div>
        </div>

      </div>

      <div className='flex flex-col justify-evenly gap-10 pt-3 border-primary-light/[0.2]'>

        <div className="flex justify-evenly gap-6 flex-col border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
          <span className="text-lg font-bold text-center text-main-text-light dark:text-main-text-dark p-2 mt-3">وضعیت دوره</span>
          <div className="flex justify-evenly flex-wrap gap-4">
            {courseStatus.map((item) => (
              <div className="p-2" key={item.id}>
                <HoverButton title={item.name} is_active={item.is_active} handleClick={() => setCourseStatusFilter(item.id)}/>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-evenly gap-6 flex-col border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
          <span className="text-lg font-bold text-center text-main-text-light dark:text-main-text-dark p-2 mt-3">سطح</span>
          <div className="flex justify-evenly flex-wrap">
            {levelStatus.map((item) => (
              <div key={item.name} className="p-2">
                <HoverButton title={item.name} is_active={item.is_active}  handleClick={() => setLevelStatusFilter(item.id)}/>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-evenly gap-6 flex-col border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
          <span className="text-lg font-bold text-center text-main-text-light dark:text-main-text-dark p-2 mt-3">نوع قیمت گزاری</span>
          <div className="flex justify-evenly">
            {paymentStatus.map((item) => (
              <div key={item.name} className="p-2">
                <HoverButton title={item.name} is_active={item.is_active} handleClick={() => setPaymentStatusFilter(item.id)}/>
              </div>
            ))}
          </div>
        </div>

        <div className="flex justify-evenly gap-6 flex-col border-primary-light/[0.2] dark:border-primary-dark/[0.2] border-t-2 rounded-sm">
          <span className="text-lg font-bold text-center text-main-text-light dark:text-main-text-dark p-2 mt-3">زبان</span>
          <div className="flex justify-evenly">
            {languageStatus.map((item) => (
              <div key={item.name} className="p-2">
                <HoverButton title={item.name} is_active={item.is_active}/>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}



const CategoriesList = ({ item }: { item: Categories }) => {
  const [isOpen, setIsOpen] = useState(false)
  const toggleOpenCategory = () => setIsOpen(prev => !prev)

  return (
    <div className="p-2">
      <div
        key={item.slug}
        className="flex flex-col justify-evenly gap-3"
      >
        {/* Category Header */}
        <div
          onClick={toggleOpenCategory}
          className="
            flex justify-between
            cursor-pointer
            transform transition duration-200
            hover:scale-105
            hover:text-hover-dark dark:hover:text-hover-light
            hover:font-bold
          "
        >
          <span>{item.title}</span>
          <FaAngleDown
            className={`
              transform transition-transform duration-200
              ${isOpen ? '' : 'rotate-90'}
            `}
          />
        </div>

        {/* Sub-categories */}
        <div
          className={`
            overflow-hidden
            transition-[max-height] duration-300 ease-in-out
            ${isOpen ? 'max-h-[1000px]' : 'max-h-0'}
          `}
        >
          {item.sub_categories.map(sub => (
            <div
              key={sub.slug}
              className="
                flex justify-between p-1
                cursor-pointer
                transform transition duration-200
                hover:translate-x-1
                hover:text-hover-dark dark:hover:text-hover-light
                hover:font-bold
              "
            >
              <span>{sub.title}</span>
              <Image
                src={`${process.env.MEDIA_URL}${sub.icon}`}
                alt={sub.title}
                height={32}
                width={32}
                className="transition-transform duration-200 hover:scale-110"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}