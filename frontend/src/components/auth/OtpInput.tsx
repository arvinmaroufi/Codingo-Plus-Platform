"use client";

import React, { useRef, useState } from "react";
import { Input } from "../ui/Input"; // adjust path as needed



export interface OTPInputProps {
  length?: number;
  onChange: (code: string) => void;
  onComplete?: (code: string) => void;
}

export const OTPInput: React.FC<OTPInputProps> = ({
  length = 4,
  onChange,
  onComplete,
}) => {
  // Create an array of empty strings for our OTP digits.
  const [otpDigits, setOtpDigits] = useState<string[]>(
    Array.from({ length }, () => "")
  );
  // Refs for each input to allow shifting focus.
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // When a change occurs, update the state for that digit
  // and trigger parent callbacks.
  const handleChange = (index: number, value: string) => {
    // Allow only alphanumeric characters (adjust the regex if required)
    if (!/^[0-9a-zA-Z]*$/.test(value)) return;
    const newDigits = [...otpDigits];
    // Take only the last character if a user types too many characters.
    newDigits[index] = value.slice(-1);
    setOtpDigits(newDigits);

    // Update the parent with the current OTP code.
    const currentOTP = newDigits.join("");
    onChange(currentOTP);

    // Move focus to the next input if there is one.
    if (value && index < length - 1) {
      inputRefs.current[index + 1]?.focus();
    }

    // If all digits are filled, call onComplete.
    if (newDigits.every((digit) => digit !== "")) {
      onComplete && onComplete(newDigits.join(""));
    }
  };

  const handleKeyDown = (
    index: number,
    e: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (e.key === "Backspace") {
      // If current field is empty, focus previous.
      if (otpDigits[index] === "" && index > 0) {
        inputRefs.current[index - 1]?.focus();
        const newDigits = [...otpDigits];
        newDigits[index - 1] = "";
        setOtpDigits(newDigits);
        onChange(newDigits.join(""));
      } else {
        // Otherwise, clear current field.
        const newDigits = [...otpDigits];
        newDigits[index] = "";
        setOtpDigits(newDigits);
        onChange(newDigits.join(""));
      }
    }
  };

  return (
    <div className="flex gap-2">
        {Array.from({ length }).map((_, index) => (
        <Input
            key={index}
            type="text"
            maxLength={1}
            ref={(el) => {
            inputRefs.current[index] = el;
            }}
            value={otpDigits[index]}
            onChange={(e) => handleChange(index, e.target.value)}
            onKeyDown={(e) => handleKeyDown(index, e)}
            className="w-12 h-12 text-center text-lg"
        />
        ))} 
    </div>
  );
};

export default OTPInput;
