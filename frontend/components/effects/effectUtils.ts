import { CookieOptions } from 'nuxt/dist/app';

export type touch = { touchDevice: Readonly<Ref<boolean>> };

const inAYear = computed(() => {
  const date = new Date();
  const expiryDate = new Date(
    date.getFullYear() + 1,
    date.getMonth(),
    date.getDate()
  );

  const expiryTime = Math.floor((expiryDate.getTime() - date.getTime()) / 1000);
  return { expiryDate, expiryTime };
});

export const cookieOptions: CookieOptions = {
  expires: inAYear.value.expiryDate,
  maxAge: inAYear.value.expiryTime,
  sameSite: 'strict',
  secure: true
};

export function trapFocus(
  event: KeyboardEvent,
  tabLength: number,
  tabIndex: number
) {
  if (event.shiftKey) {
    if (tabIndex - 1 > -1) tabIndex--;
    else if (tabIndex - 1 === -1) tabIndex = tabLength - 1;
  } else if (tabIndex + 1 < tabLength) tabIndex++;
  else if (tabIndex + 1 === tabLength) tabIndex = 0;
  event.stopImmediatePropagation();
  event.preventDefault();
  return tabIndex;
}

export function trapFocusDescendant(
  event: KeyboardEvent,
  tabLength: number,
  tabIndex: number
) {
  if (event.key === 'ArrowUp') {
    if (tabIndex - 1 > -1) tabIndex--;
  } else if (tabIndex + 1 < tabLength) tabIndex++;
  event.stopImmediatePropagation();
  event.preventDefault();
  return tabIndex;
}

export function trapFocusHorizontal(
  event: KeyboardEvent,
  tabLength: number,
  tabIndex: number
) {
  if (event.key === 'ArrowLeft') {
    if (tabIndex - 1 > -1) tabIndex--;
    else if (tabIndex - 1 === -1) tabIndex = tabLength - 1;
  } else if (tabIndex + 1 < tabLength) tabIndex++;
  else if (tabIndex + 1 === tabLength) tabIndex = 0;
  event.stopImmediatePropagation();
  event.preventDefault();
  return tabIndex;
}
