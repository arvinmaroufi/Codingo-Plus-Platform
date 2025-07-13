interface MainCategory {
  title: string;
  slug: string;
  icon: string | null;
  description: string | null;
  created_at: string;
  updated_at: string;
}

interface SubCategory {
  parent: MainCategory;
  slug: string;
  title: string;
  icon: string;
  description: string | null;
  created_at: string;
  updated_at: string;
};

interface Teacher {
  username: string;
  full_name: string;
  joined_date: string;
};

interface Tags {
  id: number;
  name: string;
  slug: string;
  created_at: string;
  updated_at: string;
}

interface Course {
  slug: string;
  category: SubCategory;
  teacher: Teacher;
  tags: Tags[];
  is_enrolled: boolean;
  enrollment_count: number;
  review_count: number;
  title: string;
  description: string;
  duration: string;
  price: number | 0;
  payment_status: string;
  poster: string | null;
  banner: string | null;
  trailer: string | null;
  language: string;
  level_status: string;
  status: string;
  publish_status: string;
  views: number;
  published_date: string | null;
  created_at: string;
  updated_at: string;
};

export default Course;