export const allCountries = Object.freeze({
  AU: 'Australia',
  BE: 'Belgium',
  CA: 'Canada',
  DK: 'Denmark',
  EU: 'Europe',
  FR: 'France',
  GB: 'United Kingdom',
  IE: 'Ireland',
  JP: 'Japan',
  LT: 'Lithuania',
  PL: 'Poland',
  RO: 'Romania',
  SE: 'Sweden',
  US: 'United States',
  ZA: 'South Africa'
});

const enCountries = Object.freeze({
  AU: 'Australia',
  CA: 'Canada',
  EU: 'Europe',
  GB: 'United Kingdom',
  US: 'United States'
});

type countriesT = typeof enCountries;
export type countryCodesT = keyof countriesT;
// type countryNames = countriesT[keyof countriesT];

export const countryCodes = Object.keys(enCountries) as Array<countryCodesT>;
