<script setup lang="ts">
import Loader from '../effects/Loader.vue';
import ResultWindow from './ResultWindow.vue';
import Search from './Search.vue';
import { messageT, resultTemplate } from './schemas';
import { optionsArrayT } from './optionsList';

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
    pick: ['status_code', 'details'],
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
    timer.value = setInterval(() => console.log('Elapsed Time: ' + ++x), 1000);
    pendingResults.value = true;
    const { data: results } = await useLazyFetch<resultTemplate | messageT>(
      server + '/search',
      {
        method: 'post',
        watch: false,
        server: false,
        body: {
          searchString,
          searchParams,
        },
      }
    );
    clearInterval(timer.value);
    if (results.value !== null) {
      if (results.value.status_code !== 200)
        console.error((results.value as messageT).details);
      else _searchResults.value = results.value as resultTemplate;
    }
    pendingResults.value = false;
  } catch (error) {
    console.error('Error when retrieving search results\n', { error });
  }
}

provide('api', { searchResults, getSearchResults });

const mainContainer =
  'flex flex-col w-full h-fit self-center grow border-b-2 relative shadow-md ' +
  'transition border-slate-200 dark:border-slate-700 ';
</script>

<template>
  <main :class="mainContainer">
    <Search />
    <ResultWindow v-if="awake && !pendingResults" />
    <Loader v-else-if="awake && pendingResults" loaderText="Loading" />
    <Loader v-else loaderText="Connecting" />
  </main>
</template>
