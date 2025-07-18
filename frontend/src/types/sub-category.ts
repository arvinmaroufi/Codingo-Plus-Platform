import MainCategory from "./main-category";

interface SubCategory {
  main_category: MainCategory;
  slug: string;
  title: string;
  icon: string;
  description: string;
  created_at: string;
  updated_at: string;
};

export default SubCategory;