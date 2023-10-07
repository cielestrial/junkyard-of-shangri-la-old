type countriesT = typeof en_countries;
export type countryCodesT = keyof countriesT;
// type countryNames = countriesT[keyof countriesT];

const all_countries = Object.freeze({
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
  ZA: 'South Africa',
});
export const en_countries = Object.freeze({
  AU: 'Australia',
  CA: 'Canada',
  EU: 'Europe',
  GB: 'United Kingdom',
  US: 'United States',
});

export const countryCodes = Object.keys(en_countries) as Array<countryCodesT>;
