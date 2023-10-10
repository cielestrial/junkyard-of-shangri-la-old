<script setup lang="ts">
  import MyLoader from '../effects/MyLoader.vue';
  import ResultWindow from './ResultWindow.vue';
  import { optionsArrayT } from './optionsList';
  import { messageT, orderByT, orderFromT, resultTemplate } from './schemas';
  import SearchForm from './search/SearchForm.vue';

  const server =
    process.env.NODE_ENV === 'production' ? '' : 'http://127.0.0.1:8000';

  const _searchResults = ref<resultTemplate>({} as resultTemplate);
  const searchResults = readonly(_searchResults);
  const pendingResults = ref(false);
  const awake = ref(false);
  const timer = ref<NodeJS.Timeout>();

  const { data: ping, error: pingError } = useLazyFetch<messageT>(
    server + '/ping',
    {
      method: 'get',
      watch: false,
      server: false,
      pick: ['status_code', 'details']
    }
  );

  watch(ping, (newVal) => {
    if (newVal !== null) {
      if (newVal.status_code !== 200) console.error(newVal.details);
      else if (!awake.value && newVal.details === 'pong') awake.value = true;
    }
  });

  watch(pingError, (newVal) => {
    if (newVal !== null)
      console.error('Error when pinging server:\n', { newVal });
  });

  async function getSearchResults(
    searchString: string,
    searchParams: optionsArrayT
  ) {
    try {
      let x = 0;
      clearInterval(timer.value);
      timer.value = setInterval(
        () => console.log('Elapsed Time: ' + ++x),
        1000
      );
      pendingResults.value = true;
      const { data: results } = await useLazyFetch<resultTemplate | messageT>(
        server + '/search',
        {
          method: 'post',
          watch: false,
          server: false,
          body: {
            searchString,
            searchParams
          }
        }
      );
      clearInterval(timer.value);
      if (results.value !== null) {
        if (results.value.status_code !== 200)
          console.error((results.value as messageT).details);
        else {
          _searchResults.value = results.value as resultTemplate;
          if (_searchResults.value.total > 1) sortBy('price', 'least');
        }
      }
      pendingResults.value = false;
    } catch (error) {
      console.error('Error when retrieving search results\n', { error });
    }
  }

  onBeforeUnmount(() => {
    clearInterval(timer.value);
  });

  function sortBy(orderBy: orderByT, orderFrom: orderFromT) {
    _searchResults.value.results.sort((a, b) => {
      if (orderBy === 'price') {
        const re = /[\D.]/g;
        const aVal = +a.price.replace(re, '');
        const bVal = +b.price.replace(re, '');
        if (orderFrom === 'least') return aVal - bVal;
        else return bVal - aVal;
      } else if (orderFrom === 'least')
        return a.category.localeCompare(b.category);
      else return b.category.localeCompare(a.category);
    });
  }

  provide('api', { searchResults, getSearchResults });

  const mainContainer =
    'flex flex-col w-full h-fit self-center grow relative shadow-md ' +
    'transition dark:shadow-gray-900/50 ';
</script>

<template>
  <main id="main" role="main" :class="mainContainer">
    <SearchForm />
    <ResultWindow v-if="awake && !pendingResults" />
    <MyLoader v-else-if="awake && pendingResults" loader-text="Loading" />
    <MyLoader v-else loader-text="Connecting" />
  </main>
</template>
