<script setup lang="ts">
import MyAnimations from '~/components/effects/MyAnimations.vue';
import MyOverlay from '~/components/effects/MyOverlay.vue';
import { trapFocusDescendant } from '~/components/effects/effectUtils';
import { theme } from '~/pages/index.vue';
import BIcons from '../../icons/BIcons.vue';
import Flags_EN from './En_Flags.vue';
import { countryCodes, countryCodesT, en_countries } from './countryData';

const { colorScheme } = inject('theme') as theme;

const comboboxRef = ref<HTMLUListElement | null>(null);
const listboxRef = ref<HTMLUListElement | null>(null);

const tabList = ref<NodeListOf<Element>>();
const tabLength = ref(-1);
const tabIndex = ref(-1);

const opened = ref(false);
const options = ref(countryCodes);
const selected = ref<countryCodesT>('CA');

const TAInput = ref<string[]>([]);
const re = /^[a-z]$/i;
const timer = ref<NodeJS.Timeout>();

onMounted(() => {
  window.localStorage.removeItem('country_code');
  const local: any = window.localStorage.getItem('country');
  if (local === null) return;
  if (options.value.includes(local)) selected.value = local;
});

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
  window.localStorage.setItem('country', newVal);
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
      opened.value = false;
      event.stopImmediatePropagation();
    }
  } else if (event.key === 'Tab')
    menuHandler(
      tabList.value?.[tabIndex.value]?.id as countryCodesT | undefined
    );
  else if (event.key === 'Enter' || event.key === ' ') {
    handleCombobox();
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
    (tabList.value?.[tabIndex.value] as HTMLButtonElement)?.scrollIntoView(
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
    'hover:bg-gray-300 relative z-20 shadow ' +
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
  'w-full h-10 flex px-2 border-t-2 hover:bg-gray-300 ' +
  'border-gray-700 dark:border-gray-400 ';
</script>

<template>
  <button
    type="button"
    role="combobox"
    aria-controls="myListbox"
    :aria-expanded="opened"
    aria-autocomplete="none"
    :aria-activedescendant="tabList?.[tabIndex]?.id"
    aria-label="Country"
    ref="comboboxRef"
    class="rounded"
    @keydown="keyboardHandler"
  >
    <MyOverlay
      z="z-10"
      invisible
      v-if="opened"
      @click="
        () => {
          opened = false;
          menuHandler(tabList?.[tabIndex]?.id as countryCodesT | undefined);
        }
      "
    />
    <div :class="select" @click="toggle">
      <div class="flex">
        <Flags_EN class="mr-2 my-auto" :country="selected" size="2rem" />
        <span
          class="my-auto text-left"
          aria-selected="true"
          :aria-label="en_countries[selected]"
        >
          {{ selected }}
        </span>
      </div>
      <BIcons :class="caret" icon="caret-down-fill" size="1rem" />
    </div>

    <MyAnimations name="slide">
      <ol
        id="myListbox"
        role="listbox"
        ref="listboxRef"
        v-if="opened"
        :class="dropdownList"
      >
        <li
          v-for="(option, key) in options"
          :key="key"
          :id="option"
          role="option"
          :aria-selected="option === selected"
          :aria-label="
            tabList?.[tabIndex]?.id !== undefined
              ? en_countries[tabList?.[tabIndex]?.id as countryCodesT]
              : undefined
          "
          @click="() => menuHandler(option)"
          :class="{
            'my-active': option === selected,
            'my-focus': option === tabList?.[tabIndex]?.id,
          }"
        >
          <div :class="dropdownItem">
            <Flags_EN class="mr-2 my-auto" :country="option" size="2.5rem" />
            <span class="my-auto text-left">{{ option }}</span>
          </div>
        </li>
      </ol>
    </MyAnimations>
  </button>
</template>
