export type touch = { touchDevice: Readonly<Ref<boolean>> };

export function trapFocus(
  event: KeyboardEvent,
  tabLength: number,
  tabIndex: number
) {
  if (event.shiftKey) {
    if (tabIndex - 1 > -1) tabIndex--;
    else if (tabIndex - 1 === -1) tabIndex = tabLength - 1;
  } else {
    if (tabIndex + 1 < tabLength) tabIndex++;
    else if (tabIndex + 1 === tabLength) tabIndex = 0;
  }
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
  } else {
    if (tabIndex + 1 < tabLength) tabIndex++;
  }
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
  } else {
    if (tabIndex + 1 < tabLength) tabIndex++;
    else if (tabIndex + 1 === tabLength) tabIndex = 0;
  }
  event.stopImmediatePropagation();
  event.preventDefault();
  return tabIndex;
}
