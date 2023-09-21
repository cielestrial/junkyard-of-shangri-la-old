type countriesT = typeof _en_countries;
export type countryCodesT = keyof countriesT;
// export type countryNames = countriesT[keyof countriesT];

const _all_countries = Object.freeze({
  AU: "Australia",
  BE: "Belgium",
  CA: "Canada",
  DK: "Denmark",
  EU: "Europe",
  FR: "France",
  GB: "United Kingdom",
  IE: "Ireland",
  JP: "Japan",
  LT: "Lithuania",
  PL: "Poland",
  RO: "Romania",
  SE: "Sweden",
  US: "United States",
  ZA: "South Africa",
});
const _en_countries = Object.freeze({
  AU: "Australia",
  CA: "Canada",
  EU: "Europe",
  GB: "United Kingdom",
  US: "United States",
});

export const countryCodes = Object.keys(_en_countries) as Array<countryCodesT>;

export default { _all_countries };
