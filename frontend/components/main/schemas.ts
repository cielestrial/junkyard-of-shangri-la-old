import { optionsArrayT } from './optionsList';

interface productTemplate {
  image: string;
  name: string;
  price: string;
  status: string;
  link: string;
}

export interface api {
  searchResults: Readonly<
    globalThis.Ref<{
      readonly total: number;
      readonly results: readonly productTemplate[];
    }>
  >;

  getSearchResults: (
    searchString: string,
    searchParams: optionsArrayT
  ) => Promise<void>;
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
