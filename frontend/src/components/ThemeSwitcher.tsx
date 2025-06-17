'use client';


import {FiSun, FiMoon, FiAtSign} from 'react-icons/fi'
import { useState, useEffect } from 'react';
import Image from 'next/image';
import { useTheme } from 'next-themes';

export default function ThemeSwitcher() {
    const [mounted, setMounted] = useState(false)
    const { setTheme, resolvedTheme } = useTheme()

    useEffect(() => setMounted(true), [])

    if (!mounted) return(
        <FiAtSign />
    )

    if (resolvedTheme === 'dark') {
        return(
            <div className="cursor-pointer">
                <FiSun onClick={() => setTheme('light')} />
            </div>
        ) 
    }

    if (resolvedTheme === 'light') {
        return (
            <div className="cursor-pointer">
                <FiMoon onClick={() => setTheme('dark')} />
            </div>
        )
    }
}