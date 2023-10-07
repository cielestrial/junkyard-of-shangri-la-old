<script setup lang="ts">
import MyAnimations from '~/components/effects/MyAnimations.vue';
import MyOverlay from '~/components/effects/MyOverlay.vue';
import BIcons from '~/components/icons/BIcons.vue';
import { optionsArrayT, optionsList } from '../optionsList';
import { api } from '../schemas';
import Options from './Options.vue';

const { getSearchResults } = inject('api') as api;

const searchBarRef = ref<HTMLInputElement | null>(null);
const searchButtonRef = ref<HTMLButtonElement | null>(null);
const optionsButtonRef = ref<HTMLButtonElement | null>(null);

const searchItem = ref('');
const opened = ref(false);

const searchError = ref<string | null>(null);
const optionsError = ref<string | null>(null);

const searchOptions = ref<optionsArrayT>(optionsList);
const _selectedOptions = ref<optionsArrayT | []>(searchOptions.value);
const selectedOptions = readonly(_selectedOptions);

onMounted(() => {
  window.localStorage.removeItem('selected_options');
  const local = window.localStorage.getItem('selectedOptions');
  if (local === null) return;
  const parsed = JSON.parse(local);
  let flag = true;
  if (parsed instanceof Array) {
    for (let i = 0, len = parsed.length; i < len; i++) {
      flag = optionsList.includes(parsed[i]);
      if (!flag) break;
    }
    if (flag) _selectedOptions.value = parsed;
  }
});

watch([searchItem, opened], ([newString, newValue]) => {
  if (newValue === false) validate('option');
  if (newString !== '') validate('search');
});

watch(_selectedOptions, (newVal) => {
  if (newVal.length > 0)
    window.localStorage.setItem('selectedOptions', JSON.stringify(newVal));
});

function setSelectedOptions(selected: optionsArrayT | []) {
  _selectedOptions.value = selected;
}

function submitForm(event: Event) {
  event.preventDefault();
  if (searchBarRef.value !== null) searchBarRef.value.blur();
  checkForm();
}

function checkForm() {
  validate('both');
  if (!searchError.value && !optionsError.value)
    getSearchResults(searchItem.value, _selectedOptions.value);
  else if (searchError.value && searchBarRef.value !== null)
    searchBarRef.value.focus();
  else if (optionsError.value && optionsButtonRef.value !== null)
    optionsButtonRef.value.focus();
}

function validate(form: 'search' | 'option' | 'both') {
  if (form === 'both' || form === 'search') {
    if (searchItem.value !== '') {
      const re = /^(?:\w+[-\+']?\w* ?)+$/gi;
      const isValid = re.test(searchItem.value);
      if (!isValid) searchError.value = 'Invalid product name.';
      else searchError.value = null;
    } else searchError.value = 'Enter product name.';
  }

  if (form === 'both' || form === 'option') {
    if (_selectedOptions.value.length === 0)
      optionsError.value = 'At least one category must be selected.';
    else optionsError.value = null;
  }
}

function close() {
  opened.value = false;
  optionsButtonRef.value?.focus();
}

provide('options', { selectedOptions, setSelectedOptions });

/*
function updateText() {
  if (inputRef.value !== null) searchItem.value = inputRef.value.value;
}
*/

const border = 'border-4 rounded transition ';
const searchGroup =
  'w-fit h-fit flex flex-wrap justify-center gap-2 px-2 sm:px-5 mx-auto mb-4 ';
const searchBar = computed(
  () =>
    'w-64 sm:w-[20rem] lg:w-[35rem] h-14 font-bold text-black/90 bg-white ' +
    'dark:text-white/90 dark:bg-gray-800 shadow dark:shadow-gray-900/50 ' +
    'bg-no-repeat bg-[0.5rem] pl-10 pr-2 ' +
    'bg-search-light dark:bg-search-dark ' +
    (searchError.value
      ? 'border-red-400 '
      : 'border-gray-700 dark:border-gray-400 ') +
    border
);
const _button =
  'w-fit h-14 shadow dark:shadow-gray-900/50 p-2 ' +
  'active:scale-95 active:bg-gray-400 hover:bg-gray-300 ' +
  //  'focus-visible:bg-gray-300 ' +
  'text-black/90 bg-white dark:text-white/90 dark:bg-gray-800 ' +
  border;
const searchButton =
  _button + 'font-bold border-gray-700 dark:border-gray-400 ';
const optionsButton = computed(
  () =>
    _button +
    (optionsError.value
      ? 'border-red-400 '
      : 'border-gray-700 dark:border-gray-400 ')
);
</script>

<template>
  <form
    id="search"
    role="search"
    class="w-full h-fit mx-auto mt-5 mb-12 relative"
    action="/"
    method="post"
    novalidate
    @sumbit.prevent
  >
    <div :class="searchGroup">
      <!-- v-model doesn't work with IME languages like Japanese -->
      <!--  incase:     @compositionupdate="updateText" -->
      <input
        ref="searchBarRef"
        id="searchBar"
        name="searchBar"
        type="search"
        :class="searchBar"
        v-model.lazy.trim="searchItem"
        maxlength="100"
        autocomplete="off"
        required
        aria-autocomplete="none"
        @keydown.enter="submitForm"
        :aria-invalid="searchError !== null"
        aria-describedby="searchError"
      />
      <span class="flex flex-nowrap gap-2">
        <button
          ref="searchButtonRef"
          id="searchButton"
          name="searchButton"
          type="submit"
          :class="searchButton"
          @click="submitForm"
        >
          Search
        </button>

        <button
          ref="optionsButtonRef"
          id="optionsButton"
          name="optionsButton"
          type="button"
          :class="optionsButton"
          @click="opened = !opened"
          aria-label="Search Options"
          aria-required="true"
          :aria-invalid="optionsError !== null"
          aria-describedby="optionsError"
        >
          <BIcons
            class="rounded-full mx-2 -rotate-45"
            icon="gear-fill"
            size="1.5rem"
          />
        </button>
      </span>

      <Teleport to="body">
        <MyAnimations name="fade">
          <MyOverlay z="z-20" v-if="opened" />
        </MyAnimations>
        <MyAnimations name="scale">
          <Options v-if="opened" @close="close" />
        </MyAnimations>
      </Teleport>
    </div>
    <div class="w-full flex h-fit text-red-400">
      <span class="w-40 min-h-40 sm:w-80 md:w-[30rem] mx-auto">
        <ul class="flex flex-col gap-2 list-outside list-disc">
          <li v-if="searchError">
            <p id="searchError">{{ searchError }}</p>
          </li>
          <li v-if="optionsError">
            <p id="optionsError">{{ optionsError }}</p>
          </li>
        </ul>
      </span>
    </div>
  </form>
</template>
