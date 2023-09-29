<script setup lang="ts">
import MyAnimations from '../effects/MyAnimations.vue';
import Overlay from '../effects/Overlay.vue';
import BIcons from '../icons/BIcons.vue';
import { optionsArrayT, optionsList } from './optionsList';
import { api, theme } from './schemas';

const { colorScheme } = inject('theme') as theme;
const { getSearchResults } = inject('api') as api;

const searchItem = ref('');
const allRef = ref<HTMLInputElement | null>(null);
const allChecked = ref(false);
const opened = ref(false);
const errors = ref<string[]>([]);
const searchOptions = ref<optionsArrayT>(optionsList);
const optionLength = searchOptions.value.length;
const selectedSearchOptions = ref<optionsArrayT | []>(searchOptions.value);
const scrollRef = ref<HTMLElement | null>(null);
const searchError = ref(false);
const optionsError = ref(false);

watch(allRef, (val) => {
  if (val !== null) handleAllOnChange();
});
watch(selectedSearchOptions, handleAllOnChange);
watch([searchItem, opened], ([newString, newValue]) => {
  if (newValue === false) validate('option');
  if (newString !== '') validate('search');
});

function checkForm(e: Event) {
  validate('both');
  if (errors.value.length === 0)
    getSearchResults(searchItem.value, selectedSearchOptions.value);
  e.preventDefault();
}
function validate(form: 'search' | 'option' | 'both') {
  errors.value = [];
  searchError.value = false;
  optionsError.value = false;

  if (form === 'both' || form === 'search') {
    if (searchItem.value !== '') {
      const re = /^(?:\w+[-\+']?\w* ?)+$/gi;
      const isValid = re.test(searchItem.value);
      if (!isValid) {
        errors.value.push('Invalid product name.');
        searchError.value = true;
      }
    } else {
      errors.value.push('Enter product name.');
      searchError.value = true;
    }
  }

  if (form === 'both' || form === 'option') {
    if (selectedSearchOptions.value.length === 0) {
      errors.value.push('At least one category must be selected.');
      optionsError.value = true;
    }
  }
}
/*
function updateText() {
  if (inputRef.value !== null) searchItem.value = inputRef.value.value;
}
*/
function handleAllOnClick() {
  if (allRef.value !== null) {
    if (allChecked.value) selectedSearchOptions.value = [];
    else selectedSearchOptions.value = searchOptions.value;
  }
}

function handleAllOnChange() {
  if (allRef.value !== null) {
    const length = selectedSearchOptions.value.length;
    allChecked.value = false;
    allRef.value.indeterminate = false;
    if (length === optionLength) {
      allChecked.value = true;
    } else if (length !== 0) {
      allRef.value.indeterminate = true;
    }
  }
}

function parallelScroll(e: WheelEvent) {
  if (scrollRef.value !== null) {
    const scrollBy = Math.floor(scrollRef.value.scrollWidth * 0.1);
    if (e.deltaY > 0) scrollRef.value.scrollLeft += scrollBy;
    else if (e.deltaY < 0) scrollRef.value.scrollLeft -= scrollBy;
  }
}

const border = 'border-4 rounded transition ';
const searchBar = computed(
  () =>
    'w-[70vmin] h-14 px-[2vmin] shadow-md text-black/90 bg-white ' +
    'dark:text-white/90 dark:bg-slate-800 font-bold ' +
    (searchError.value
      ? 'border-red-400 '
      : 'border-slate-700 dark:border-slate-400 ') +
    border
);
const _button =
  'w-fit h-14 shadow-md p-2 hover:bg-slate-300 ' +
  'active:scale-95 active:bg-slate-400 ' +
  'text-black/90 bg-white dark:text-white/90 dark:bg-slate-800 ' +
  border;

const searchButton =
  _button + 'font-bold border-slate-700 dark:border-slate-400 ';

const optionsButton = computed(
  () =>
    _button +
    (optionsError.value
      ? 'border-red-400 '
      : 'border-slate-700 dark:border-slate-400 ')
);

const checkboxOuterArea =
  'z-20 w-fit h-fit m-auto shadow-md select-none ' + border + colorScheme;

const checkboxInnerArea =
  'w-[80vmin] aspect-square m-[1.5vmin] px-[1.5vmin] ' + border + colorScheme;

const checkboxGroup =
  'flex flex-col flex-wrap w-full h-full list-outside pl-[1.5vmin] ' +
  'gap-x-2 gap-y-0.5 overflow-auto scroll-smooth overscroll-none ';
</script>

<template>
  <div id="search" class="w-full h-fit mx-auto mt-5 relative">
    <form action="/" method="post" novalidate @submit="checkForm">
      <div id="search_group" class="w-fit h-fit flex m-auto gap-2">
        <!-- v-model doesn't work with IME languages like Japanese -->
        <!--  incase:     @compositionupdate="updateText" -->
        <input
          :class="searchBar"
          type="search"
          id="q"
          name="q"
          v-model.lazy.trim="searchItem"
          placeholder="Product"
          aria-required="true"
          required
          maxlength="100"
          autocomplete="off"
        />

        <button id="submit" type="submit" :class="searchButton">Search</button>

        <button type="button" :class="optionsButton" @click="opened = !opened">
          <BIcons
            class="rounded-full mx-2 -rotate-45"
            icon="gear-fill"
            size="1.5rem"
          />
        </button>
        <Teleport to="body">
          <MyAnimations name="fade">
            <Overlay z="z-20" v-if="opened" />
          </MyAnimations>
          <MyAnimations name="scale">
            <Overlay z="z-20" v-if="opened" invisible>
              <Overlay z="z-20" invisible @click="opened = false" />
              <div :class="checkboxOuterArea">
                <div :class="checkboxInnerArea">
                  <div class="w-full h-fit flex justify-between pt-2 pb-1">
                    <div class="w-fit h-fit flex gap-x-1 pt-2">
                      <input
                        ref="allRef"
                        type="checkbox"
                        id="all"
                        class="cursor-pointer"
                        :checked="allChecked"
                        @change="handleAllOnClick"
                      />
                      <label for="all" class="cursor-pointer font-bold">
                        All
                      </label>
                    </div>
                    <button
                      type="button"
                      @click="opened = false"
                      class="w-fit h-fit text-red-500 bg-white rounded"
                    >
                      <BIcons icon="x-square-fill" size="1.5rem" />
                    </button>
                  </div>

                  <ul
                    ref="scrollRef"
                    :class="checkboxGroup"
                    @wheel="parallelScroll"
                  >
                    <li v-for="(option, key) in searchOptions" :key="key">
                      <div class="flex gap-x-1">
                        <input
                          type="checkbox"
                          name="websites"
                          :id="option"
                          :value="option"
                          v-model="selectedSearchOptions"
                          class="cursor-pointer"
                        />
                        <label
                          :for="option"
                          class="cursor-pointer whitespace-nowrap"
                        >
                          {{ option }}
                        </label>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>
            </Overlay>
          </MyAnimations>
        </Teleport>
      </div>

      <div class="w-full flex h-14 mt-1 mb-2.5 text-red-400 relative z-0">
        <div v-if="errors.length !== 0" class="w-[30rem] mx-auto">
          <ul class="flex flex-col list-outside list-disc">
            <li class="mt-1.5" v-for="error in errors">
              {{ error }}
            </li>
          </ul>
        </div>
      </div>
    </form>
  </div>
</template>
