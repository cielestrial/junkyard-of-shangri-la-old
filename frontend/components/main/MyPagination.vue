<script setup lang="ts">
import { pages } from './schemas';

const { pageIndex, totalPages, setPageIndex } = inject('pages') as pages;
console.log('total=' + totalPages.value);
watch(pageIndex, (newVal) =>
  console.log('page=' + (newVal === totalPages.value - 1))
);

function indexRange(position: number) {
  if (pageIndex.value <= 1) return position + 1;
  else if (pageIndex.value > 1 && pageIndex.value + 2 < totalPages.value) {
    if (position === 1) return pageIndex.value;
    else if (position === 2) return pageIndex.value + 1;
    else return pageIndex.value + 2;
  } else return position + totalPages.value - 4;
}

const button =
  'w-10 rounded border-4 transition shadow-md ' +
  'active:scale-95 hover:bg-slate-300 ' +
  'text-black/90 bg-white border-slate-700 ' +
  'dark:text-white/90 dark:bg-slate-800 dark:border-slate-400 ';
const ellipsis = 'w-10 text-center pt-1.5 -mx-2';
</script>

<template>
  <div class="flex flex-nowrap w-fit mx-auto gap-2 mb-2">
    <button
      type="button"
      :class="[button, { myActive: pageIndex + 1 === 1 }]"
      @click="setPageIndex(1)"
    >
      1
    </button>

    <span :class="ellipsis" v-if="totalPages > 5 && pageIndex > 2">
      &hellip;
    </span>

    <button
      v-if="totalPages > 2"
      v-for="i in Math.min(totalPages - 2, 3)"
      :key="i"
      type="button"
      :class="[button, { myActive: pageIndex + 1 === indexRange(i) }]"
      @click="setPageIndex(indexRange(i))"
    >
      {{ indexRange(i) }}
    </button>

    <span :class="ellipsis" v-if="totalPages > 5 && totalPages - pageIndex > 3">
      &hellip;
    </span>

    <button
      v-if="totalPages > 1"
      type="button"
      :class="[button, { myActive: pageIndex + 1 === totalPages }]"
      @click="setPageIndex(totalPages)"
    >
      {{ totalPages }}
    </button>
  </div>
</template>
