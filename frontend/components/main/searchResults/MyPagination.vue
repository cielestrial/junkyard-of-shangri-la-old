<script setup lang="ts">
  import { computed, inject, ref, watch } from 'vue-demi';
  import { pages } from '../schemas';
  import BIcons from '~/components/icons/BIcons.vue';
  import { theme } from '~/pages/index.vue';

  defineProps<{ pos: 'top' | 'bottom' }>();

  const { colorScheme } = inject('theme') as theme;
  const { pageIndex, totalPages, setPageIndex } = inject('pages') as pages;

  const prevButtonRef = ref<HTMLButtonElement | null>();
  const nextButtonRef = ref<HTMLButtonElement | null>();

  const totalRotatingButtons = computed(() =>
    Math.min(totalPages.value - 2, 3)
  );
  const rotatingButtons = ref<number[]>([-1]);

  watch(
    totalPages,
    () => {
      rotatingButtons.value = [-1];
      for (let i = 1; i <= totalRotatingButtons.value; i++)
        rotatingButtons.value.push(indexRange(i));
    },
    { immediate: true }
  );

  watch(
    pageIndex,
    () => {
      for (let i = 1; i <= totalRotatingButtons.value; i++)
        rotatingButtons.value[i] = indexRange(i);
    },
    { immediate: false }
  );

  function indexRange(position: number) {
    let result: number, lowerbound: number, upperbound: number;
    // lowerbound off of index + 1, index + 1 + position
    // upperbound off of total, total - 4 + position
    lowerbound = pageIndex.value - 1 + position;
    upperbound = totalPages.value - 4 + position;
    // if index=1, total=6, total-1=5, total-4=2, pos=1
    // lower=2 , upper=3
    // lower=2 , upper=3
    // returns 2
    // pi+1 - 2 = 4 - 2 , pi-1 = 2

    // if index=2, total=6, total-1=5, total-4=2, pos=1
    // lower=3 , upper=3
    // lower=3 , upper=3
    // returns 3

    lowerbound = bind(lowerbound, position);
    upperbound = bind(upperbound, position);
    if (lowerbound < upperbound) result = lowerbound;
    else result = upperbound;
    return result;
  }

  function bind(bound: number, pos: number) {
    const lowestbound = 1 + pos;
    const uppestbound = totalPages.value - 1;
    if (bound < lowestbound) return lowestbound;
    else if (bound > uppestbound) return uppestbound;
    else return bound;
  }

  function paginationNavigation(event: KeyboardEvent) {
    if (event.key === 'ArrowLeft') {
      prevButtonRef.value?.focus();
      prevButtonRef.value?.click();
    } else if (event.key === 'ArrowRight') {
      nextButtonRef.value?.focus();
      nextButtonRef.value?.click();
    }
    event.stopImmediatePropagation();
  }

  const pagination =
    'flex flex-wrap justify-center mb-4 text-xl leading-none select-none z-10 ';
  const cell = 'w-9 aspect-square rounded ';
  const ellipsisCell = 'flex -mx-1 items-end ' + cell;
  const ellipsis = 'h-fit mx-auto mb-1 rounded ';
  const button =
    'border-2 shadow active:scale-95 active:bg-gray-300 ' +
    'dark:active:bg-gray-600 hover:bg-gray-200 dark:hover:bg-gray-500 ' +
    cell +
    colorScheme;
</script>

<template>
  <nav
    :id="`${pos}Pagination`"
    role="navigation"
    :aria-label="`${pos} pagination`"
    :class="pagination"
    @keydown="paginationNavigation"
  >
    <span class="flex flex-nowrap justify-center">
      <button
        ref="prevButtonRef"
        aria-label="Goto Previous Page"
        type="button"
        class="m-1 rounded cursor-default"
        :aria-disabled="pageIndex + 1 === 1 || totalPages === 1"
        @click="
          () => {
            if (prevButtonRef?.ariaDisabled === 'false')
              setPageIndex(pageIndex - 1);
          }
        "
      >
        <span
          :class="[
            button,
            'flex cursor-pointer',
            { 'my-disabled': pageIndex + 1 === 1 || totalPages === 1 }
          ]"
        >
          <BIcons class="m-auto -rotate-90" icon="chevron-up" size="1rem" />
        </span>
      </button>

      <button
        :aria-label="(pageIndex + 1 === 1 ? '' : 'Goto ') + 'Page 1'"
        :aria-current="pageIndex + 1 === 1"
        type="button"
        :class="[button, 'm-1', { 'my-active': pageIndex + 1 === 1 }]"
        @click="setPageIndex(0)"
      >
        1
      </button>

      <div
        v-if="totalPages > 5 && pageIndex > 2"
        aria-label="ellipsis"
        tabindex="-1"
        :class="ellipsisCell"
      >
        <BIcons :class="ellipsis" icon="three-dots" size="1rem" />
      </div>
    </span>

    <span v-if="totalPages > 2" class="flex flex-nowrap justify-center">
      <button
        v-for="i in totalRotatingButtons"
        :key="i"
        type="button"
        :aria-label="
          (pageIndex + 1 === rotatingButtons[i] ? '' : 'Goto ') +
          `Page ${rotatingButtons[i]}`
        "
        :aria-current="pageIndex + 1 === rotatingButtons[i]"
        :class="[
          button,
          'm-1',
          { 'my-active': pageIndex + 1 === rotatingButtons[i] }
        ]"
        @click="setPageIndex(rotatingButtons[i] - 1)"
      >
        {{ rotatingButtons[i] }}
      </button>
    </span>

    <span class="flex flex-nowrap justify-center">
      <div
        v-if="totalPages > 5 && totalPages - pageIndex > 3"
        aria-label="ellipsis"
        tabindex="-1"
        :class="ellipsisCell"
      >
        <BIcons :class="ellipsis" icon="three-dots" size="1rem" />
      </div>

      <button
        v-if="totalPages > 1"
        :aria-label="
          (pageIndex + 1 === totalPages ? '' : 'Goto ') + `Page ${totalPages}`
        "
        :aria-current="pageIndex + 1 === totalPages"
        type="button"
        :class="[button, 'm-1', { 'my-active': pageIndex + 1 === totalPages }]"
        @click="setPageIndex(totalPages - 1)"
      >
        {{ totalPages }}
      </button>

      <button
        ref="nextButtonRef"
        aria-label="Goto Next Page"
        type="button"
        :aria-disabled="pageIndex + 1 === totalPages || totalPages === 1"
        class="m-1 rounded cursor-default"
        @click="
          () => {
            if (nextButtonRef?.ariaDisabled === 'false')
              setPageIndex(pageIndex + 1);
          }
        "
      >
        <span
          :class="[
            button,
            'flex cursor-pointer',
            { 'my-disabled': pageIndex + 1 === totalPages || totalPages === 1 }
          ]"
        >
          <BIcons class="m-auto rotate-90" icon="chevron-up" size="1rem" />
        </span>
      </button>
    </span>
  </nav>
</template>
