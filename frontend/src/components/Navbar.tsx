"use client";

import { FaHome, FaMedal, FaRegFileCode } from "react-icons/fa";
import { MdOutlineLibraryBooks } from "react-icons/md";
import { FloatingNav } from "./ui/FloatingNavbar";


interface NavItem {
  name: string;
  href: string;
  icon?: React.ReactNode;
}


export default function Navbar() {
  const navItems = [
        { name: "خانه", href: "/", icon: <FaHome /> },
        { name: "درباره", href: "/about", icon: <FaMedal /> },
        { name: "دوره‌ها", href: "/projects", icon: <FaRegFileCode /> },
        { name: "وبلاگ", href: "/blogs", icon: <MdOutlineLibraryBooks /> },
        { name: "مشاوره", href: "/consult", icon: <MdOutlineLibraryBooks /> },
  ]

  return (
    <FloatingNav navItems={navItems}/>
  );
}
