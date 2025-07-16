export const courseFiltersData = {
    courseStatus: [
        {
            id: 1,
            name: "تکمیل شده",
            value: "C",
            is_active: false,
        },
        {
            id: 2,
            name: "درحال برگزاری",
            value: "I",
            is_active: false,
        },
        {
            id: 3,
            name: "شروع به زودی",
            value: "S",
            is_active: false,
        }
    ],
    levelStatus: [
        {
            id: 1,
            name: "مقدماتی",
            value: "IN",
            is_active: false,
        },
        {
            id: 2,
            name: "متوسط",
            value: "IM",
            is_active: false,
        },
        {
            id: 3,
            name: "پیشرفته",
            value: "AD",
            is_active: false,
        },
        {
            id: 4,
            name: "مقدماتی تا پیشرفته",
            value: "IA",
            is_active: false,
        }
    ],
    paymentStatus: [
        {
            id: 1,
            name: "پولی",
            value: "P",
            is_active: false,
        },
        {
            id: 2,
            name: "رایگان",
            value: "F",
            is_active: false,
        }
    ],
    languageStatus: [
        {
            id: 1,
            name: "فارسی",
            value: "FA",
            is_active: false,
        },
        {
            id: 2,
            name: "انگلیسی",
            value: "EN",
            is_active: false,
        }
    ],
    ordering: [
        {
            id: 1,
            name: "کمترین قیمت",
            value: "price",
            is_active: false,
        },
        {
            id: 2,
            name: "بیشترین قیمت",
            value: "-price",
            is_active: false,
        },

        {
            id: 3,
            name: "پربازدید ترین",
            value: "views",
            is_active: false,
        },
        {
            id: 4,
            name: "کم بازدید ترین",
            value: "-views",
            is_active: false,
        },

        {
            id: 5,
            name: "جدید تیرن",
            value: "published_date",
            is_active: false,
        },
        {
            id: 6,
            name: "قدیمی ترین",
            value: "-published_date",
            is_active: false,
        },
    ]
}