import type { ComputedRef, Ref } from 'vue-demi';
import type { optionsArrayT } from './optionsList';

export type productTemplate = {
  image: string;
  name: string;
  price: string;
  status: string;
  category: string;
  link: string;
};

export type api = {
  searchResults: Readonly<
    Ref<{
      readonly total: number;
      readonly results: readonly productTemplate[];
    }>
  >;
  resultType: Readonly<Ref<'promo' | 'search'>>;
  batchSize: Readonly<Ref<number>>;
  getSearchResults: (
    searchString: string,
    searchParams: optionsArrayT
  ) => Promise<void>;
  getPromoResults: (
    batchSize: number,
    searchParams: optionsArrayT
  ) => Promise<void>;
};

export type pages = {
  pageIndex: Ref<number>;
  totalPages: ComputedRef<number>;
  setPageIndex: (newIndex: number) => void;
};

export type options = {
  selectedOptions: Readonly<Ref<Readonly<optionsArrayT> | readonly []>>;
  setSelectedOptions: (selected: optionsArrayT | []) => void;
  errorList: Readonly<Ref<readonly string[]>>;
};

export type messageT = {
  status_code: number;
  details: string;
};

export type resultTemplate = {
  status_code: number;
  total: number;
  results: productTemplate[];
};

export type orderByT = 'price' | 'category';
export type orderFromT = 'least' | 'greatest';
