import { optionsArrayT } from './optionsList';

export interface productTemplate {
  image: string;
  name: string;
  price: string;
  status: string;
  category: string;
  link: string;
}

export interface api {
  searchResults: Readonly<
    Ref<{
      readonly total: number;
      readonly results: readonly productTemplate[];
    }>
  >;

  getSearchResults: (
    searchString: string,
    searchParams: optionsArrayT
  ) => Promise<void>;
}

export interface pages {
  pageIndex: Ref<number>;
  totalPages: ComputedRef<number>;
  setPageIndex: (newIndex: number) => void;
}

export interface options {
  selectedOptions: Readonly<Ref<Readonly<optionsArrayT> | readonly []>>;
  setSelectedOptions: (selected: optionsArrayT | []) => void;
  errorList: Readonly<Ref<readonly string[]>>;
}

export interface messageT {
  status_code: number;
  details: string;
}

export interface resultTemplate {
  status_code: number;
  total: number;
  results: productTemplate[];
}

export type orderByT = 'price' | 'category';
export type orderFromT = 'least' | 'greatest';
