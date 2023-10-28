<script setup lang="ts">
  import { computed, inject, ref, watch } from 'vue-demi';
  import { useCookie } from 'nuxt/app';
  import BIcons from '../../icons/BIcons.vue';
  import FlagsEn from './FlagsEn.vue';
  import { countryCodes, countryCodesT, allCountries } from './countryData';
  import MyAnimations from '~/components/effects/MyAnimations.vue';
  import MyOverlay from '~/components/effects/MyOverlay.vue';
  import {
    cookieOptions,
    trapFocusDescendant
  } from '~/components/effects/effectUtils';
  import { consent, theme } from '~/pages/index.vue';

  const { colorScheme } = inject('theme') as theme;

  const comboboxRef = ref<HTMLUListElement | null>(null);
  const listboxRef = ref<HTMLUListElement | null>(null);

  const tabList = ref<NodeListOf<Element>>();
  const tabLength = ref(-1);
  const tabIndex = ref(-1);

  const opened = ref(false);
  const options = ref(countryCodes);
  const selected = ref<countryCodesT>('CA');
  const { hasConsent } = inject('consent') as consent;
  const countryCookie = useCookie<any>('country', cookieOptions);

  if (
    hasConsent.value &&
    countryCookie.value !== null &&
    options.value.includes(countryCookie.value)
  )
    selected.value = countryCookie.value;

  const TAInput = ref<string[]>([]);
  const re = /^[a-z]$/i;
  const timer = ref<NodeJS.Timeout>();

  watch(listboxRef, (newVal) => {
    if (newVal !== null) {
      tabList.value = newVal.querySelectorAll('li');
      tabLength.value = tabList.value.length;
      if (tabLength.value > 0 && tabIndex.value === -1) {
        for (let i = 0; i < tabLength.value; i++)
          if (tabList.value[i].classList.contains('my-active')) {
            tabIndex.value = i;
            break;
          }
      }
    }
  });

  watch(opened, (newVal) => {
    if (!newVal) tabIndex.value = -1;
  });

  watch(selected, (newVal) => {
    if (hasConsent.value) countryCookie.value = newVal;
  });

  function menuHandler(option: countryCodesT | undefined) {
    if (option !== undefined) selected.value = option;
    opened.value = false;
  }

  function handleCombobox() {
    if (!opened.value) opened.value = true;
    else
      menuHandler(
        tabList.value?.[tabIndex.value]?.id as countryCodesT | undefined
      );
  }

  function toggle() {
    if (comboboxRef.value !== null) {
      comboboxRef.value.focus();
      opened.value = !opened.value;
    }
  }

  function keyboardHandler(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      if (opened.value) {
        if (!event.repeat) opened.value = false;
        event.stopImmediatePropagation();
      }
    } else if (event.key === 'Tab')
      menuHandler(
        tabList.value?.[tabIndex.value]?.id as countryCodesT | undefined
      );
    else if (event.key === 'Enter' || event.key === ' ') {
      if (!event.repeat) handleCombobox();
      event.preventDefault();
    } else if (event.key === 'ArrowUp' || event.key === 'ArrowDown')
      navigateDescendants(event);
    else if (re.test(event.key)) typeAhead(event);
  }

  function navigateDescendants(event: KeyboardEvent) {
    if (opened.value) {
      tabIndex.value = trapFocusDescendant(
        event,
        tabLength.value,
        tabIndex.value
      );
      (tabList.value?.[tabIndex.value] as HTMLUListElement)?.scrollIntoView(
        false
      );
    } else {
      if (event.key === 'ArrowUp') tabIndex.value = 0;
      opened.value = true;
      event.preventDefault();
    }
  }

  function typeAhead(event: KeyboardEvent) {
    if (tabList.value === undefined) return;
    clearTimeout(timer.value);
    if (TAInput.value.length + 1 === 3) TAInput.value = [];
    TAInput.value.push(event.key.toUpperCase());

    for (
      let i = 0, len = TAInput.value.length, TA = TAInput.value.join('');
      i < tabLength.value;
      i++
    ) {
      if (tabList.value[i].id.startsWith(TA)) {
        if (document.activeElement === tabList.value[i] && len === 1) continue;
        else {
          tabIndex.value = i;
          break;
        }
      }
    }
    if (!opened.value) opened.value = true;
    timer.value = setTimeout(() => (TAInput.value = []), 500);
  }

  const select = computed(
    () =>
      'w-28 h-10 rounded flex justify-between items-center px-2 border-2 ' +
      'relative z-20 shadow hover:bg-gray-200 dark:hover:bg-gray-500 ' +
      'cursor-pointer active:bg-gray-300 dark:active:bg-gray-600 ' +
      (opened.value ? 'border-b-0 rounded-bl-none rounded-br-none ' : '') +
      colorScheme
  );

  const caret = computed(
    () =>
      'my-auto ml-2 transition text-black/90 dark:text-white/90 ' +
      (opened.value ? 'rotate-180 ' : '')
  );

  const dropdownList =
    'w-28 h-fit absolute list-outside z-10 shadow ' +
    'border-2 border-t-0 rounded-br rounded-bl ' +
    colorScheme;

  const dropdownItem =
    'w-full h-10 flex px-2 border-t-2 hover:bg-gray-200 dark:hover:bg-gray-500 cursor-pointer ' +
    'active:bg-gray-300 dark:active:bg-gray-600 border-gray-700 dark:border-gray-400 ';
</script>

<template>
  <div
    ref="comboboxRef"
    tabindex="0"
    role="combobox"
    aria-controls="myListbox"
    :aria-expanded="opened"
    aria-autocomplete="none"
    :aria-activedescendant="tabList?.[tabIndex]?.id"
    aria-label="Country"
    class="rounded"
    @keydown="keyboardHandler"
  >
    <MyOverlay
      v-if="opened"
      z="z-10"
      invisible
      @click="
        () => {
          opened = false;
          menuHandler(tabList?.[tabIndex]?.id as countryCodesT | undefined);
        }
      "
    />
    <div :class="select" @click="toggle">
      <span class="flex">
        <FlagsEn class="my-auto mr-2" :country="selected" size="2rem" />
        <span class="my-auto text-left">
          {{ selected }}
        </span>
        <span class="visually-hidden"> {{ allCountries[selected] }}</span>
      </span>
      <BIcons :class="caret" icon="caret-down-fill" size="1rem" />
    </div>

    <MyAnimations name="slide-down">
      <ol
        v-show="opened"
        id="myListbox"
        ref="listboxRef"
        role="listbox"
        :class="dropdownList"
      >
        <li
          v-for="(option, key) in options"
          :id="option"
          :key="key"
          role="option"
          :aria-selected="option === selected"
          :class="{
            'my-active': option === selected,
            'my-focus': option === tabList?.[tabIndex]?.id
          }"
          @click="() => menuHandler(option)"
        >
          <div :class="dropdownItem">
            <FlagsEn class="my-auto mr-2" :country="option" size="2.5rem" />
            <span class="my-auto text-left">
              {{ option }}
            </span>
            <span class="visually-hidden"> {{ allCountries[option] }}</span>
          </div>
        </li>
      </ol>
    </MyAnimations>
  </div>
</template>
