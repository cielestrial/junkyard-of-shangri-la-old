<script setup lang="ts">
  import MyAnimations from '../effects/MyAnimations.vue';
  import SkipLinks from '../body/SkipLinks.vue';
  import BackToTop from '../body/BackToTop.vue';
  import MyPagination from './MyPagination.vue';
  import { api, productTemplate } from './schemas';
  import { theme } from '~/pages/index.vue';

  const { colorScheme } = inject('theme') as theme;
  const { searchResults, resultType, batchSize } = inject('api') as api;

  const resultWindowRef = ref<HTMLDivElement | null>(null);

  const pageIndex = ref(0);
  const resultList = computed<productTemplate[][]>(() => {
    const temp: productTemplate[][] = [];
    for (
      let i = 0, len = searchResults.value.total;
      i < len;
      i += batchSize.value
    )
      temp.push(searchResults.value.results.slice(i, i + batchSize.value));
    return temp;
  });

  const totalPages = computed(() => resultList.value.length);

  onMounted(() => {
    if (resultWindowRef.value !== null && totalPages.value > 1)
      resultWindowRef.value.focus();
  });

  function setPageIndex(newIndex: number) {
    if (newIndex === pageIndex.value || totalPages.value < 2) return;
    if (newIndex >= 0 && newIndex <= totalPages.value - 1) {
      if (resultWindowRef.value !== null) {
        pageIndex.value = newIndex;
        resultWindowRef.value.scrollIntoView(true);
      }
    }
  }

  function getItemAriaLabel(item: productTemplate) {
    const ariaLabel = [
      `Graphic of ${item.name},`,
      `Title ${item.name},`,
      `Price ${item.price},`,
      `Category ${item.category}.`
    ];
    return ariaLabel.join(' ');
  }

  provide('pages', { pageIndex, totalPages, setPageIndex });

  const resultWindow =
    'flex flex-col rounded w-[80vw] min-w-min min-h-[35vh] h-fit mb-14 mx-auto ' +
    'border-4 shadow scroll-my-36 relative text-xl leading-none ' +
    colorScheme;
  const notButton =
    'flex border-2 rounded transition shadow dark:shadow-gray-900/50 ' +
    'mx-auto px-2 py-1 w-11/12 sm:w-full ' +
    'text-black/90 bg-sky-300 border-gray-600 ' +
    'dark:text-white/90 dark:bg-gray-900 dark:border-gray-400 ';
  const resultPage =
    'w-fit mx-auto px-2 sm:px-8 pb-8 grow flex flex-wrap gap-8 ' +
    'justify-evenly list-outside scroll-my-36 relative ';
  const link =
    'flex h-fit w-44 flex-col gap-4 rounded p-2 transition ' +
    'active:scale-95 active:bg-gray-300 dark:active:bg-gray-600 ' +
    'hover:bg-gray-200 dark:hover:bg-gray-500 ';
  const value = 'transition text-emerald-500 dark:text-green-500';
</script>

<template>
  <section
    id="resultWindow"
    ref="resultWindowRef"
    role="region"
    aria-labelledby="resultWindowLabel totalResults"
    :class="resultWindow"
    @keydown.arrow-left="setPageIndex(pageIndex - 1)"
    @keydown.arrow-right="setPageIndex(pageIndex + 1)"
  >
    <label id="resultWindowLabel" class="hidden-visually">
      Search results
    </label>
    <h2
      v-if="searchResults.total >= 0"
      id="totalResults"
      class="mx-auto my-4 text-center text-2xl font-bold leading-none"
    >
      {{ searchResults.total }} items
      <span :class="value">
        {{ resultType === 'promo' ? 'On Promo' : 'In Stock' }}
      </span>
    </h2>

    <SkipLinks v-if="searchResults.total > 0" to="Footer" />
    <MyPagination v-if="searchResults.total > 0" pos="top" />

    <MyAnimations name="fade">
      <ol
        v-if="searchResults.total > 0"
        id="searchResults"
        :key="pageIndex"
        :aria-label="`Page ${pageIndex + 1} of Search Results`"
        tabindex="-1"
        :class="resultPage"
      >
        <li v-for="(result, key) in resultList[pageIndex]" :key="key">
          <a
            :aria-label="getItemAriaLabel(result)"
            :class="link"
            :href="result.link"
            target="_blank"
            rel="noreferrer noopener"
          >
            <span class="flex h-40">
              <img
                class="m-auto border border-gray-400 shadow"
                :src="result.image"
                :alt="'Image of ' + result.name"
              />
            </span>
            <span class="flex h-12 items-center">
              <p class="mx-auto line-clamp-2 text-center text-xl leading-tight">
                {{ result.name }}
              </p>
            </span>
            <p :class="'mx-auto text-center ' + value">
              {{ result.price }}
            </p>
            <span :class="notButton">
              <p class="m-auto truncate text-center">
                {{ result.category }}
              </p>
            </span>
          </a>
        </li>
      </ol>
    </MyAnimations>

    <MyPagination v-if="searchResults.total > 0" pos="bottom" />
    <BackToTop v-if="searchResults.total > 0" />
  </section>
</template>
