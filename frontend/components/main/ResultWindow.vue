<script setup lang="ts">
import { api, theme, productTemplate } from './schemas';
import MyAnimations from '../effects/MyAnimations.vue';
import MyPagination from './MyPagination.vue';

const { colorScheme } = inject('theme') as theme;
const { searchResults } = inject('api') as api;

const resultWindowRef = ref<HTMLDivElement | null>(null);
const batchSize = ref(50);
const pageIndex = ref(0);
const resultList = computed<productTemplate[][]>(() => {
  let temp: productTemplate[][] = [];
  for (let i = 0; i < searchResults.value.total; i += batchSize.value)
    temp.push(searchResults.value.results.slice(i, i + batchSize.value));
  return temp;
});

const totalPages = computed(() => resultList.value.length);

function setPageIndex(newIndex: number) {
  newIndex--;
  if (newIndex === pageIndex.value) return;
  else if (newIndex >= 0 && newIndex <= totalPages.value - 1) {
    if (resultWindowRef.value !== null) {
      pageIndex.value = newIndex;
      resultWindowRef.value.scrollIntoView(true);
    }
  }
}

provide('pages', { pageIndex, totalPages, setPageIndex });

const resultWindow =
  'flex flex-col rounded w-[75vw] min-h-[50rem] h-max mt-10 mb-14 mx-auto ' +
  'border-4 shadow-md scroll-mt-4 relative ' +
  colorScheme;

const button =
  'flex border-4 rounded transition shadow-md ' +
  'mx-auto px-2 py-1 w-full ' +
  'active:scale-95 active:bg-slate-400 hover:animate-pulse ' +
  'text-black/90 bg-sky-300 border-slate-600 ' +
  'dark:text-white/90 dark:bg-slate-900 dark:border-slate-400 ';
</script>

<template>
  <div ref="resultWindowRef" id="resultWindow" :class="resultWindow">
    <h3 v-if="searchResults.total >= 0" class="mx-auto my-4 font-bold">
      {{ searchResults.total }} items
      <span class="text-emerald-400">In Stock</span>
    </h3>
    <MyAnimations name="fade">
      <ul
        :key="pageIndex"
        v-if="searchResults.total > 0"
        class="w-fit mx-auto px-8 pb-8 grow grid grid-cols-5 gap-8 list-outside"
      >
        <li v-for="(result, key) in resultList[pageIndex]" :key="key">
          <a
            class="w-44 flex flex-col h-fit"
            :href="result.link"
            target="_blank"
            rel="noreferrer noopener"
          >
            <span class="h-40 flex p-1 mb-4">
              <img
                class="border border-slate-400 shadow m-auto"
                :src="result.image"
                :alt="'Image of ' + result.name"
              />
            </span>
            <span class="h-12 flex items-center mb-4">
              <p class="mx-auto text-center line-clamp-2">
                {{ result.name }}
              </p>
            </span>
            <p class="text-center text-emerald-400 mx-auto mb-2">
              {{ result.price }}
            </p>
            <span :class="button">
              <p class="m-auto truncate text-center">
                {{ result.category }}
              </p>
            </span>
          </a>
        </li>
      </ul>
    </MyAnimations>
    <MyPagination v-if="searchResults.total > 0" />
  </div>
</template>
