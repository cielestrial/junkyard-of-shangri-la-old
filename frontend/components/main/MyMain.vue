<script setup lang="ts">
  import MyLoader from '../effects/MyLoader.vue';
  import { touch } from '../effects/effectUtils';
  import ResultWindow from './ResultWindow.vue';
  import { optionsArrayT, optionsList } from './optionsList';
  import { messageT, orderByT, orderFromT, resultTemplate } from './schemas';
  import SearchForm from './search/SearchForm.vue';

  const server =
    process.env.NODE_ENV === 'production'
      ? 'https://scraper-of-shangri-la.onrender.com'
      : 'http://127.0.0.1:8000';

  const { touchDevice } = inject('touch') as touch;

  const _batchSize = ref(60);
  const batchSize = readonly(_batchSize);
  const _searchResults = ref<resultTemplate>({} as resultTemplate);
  const searchResults = readonly(_searchResults);
  const _resultType = ref<'promo' | 'search'>('promo');
  const resultType = readonly(_resultType);
  const pendingSearchResults = ref(false);
  const pendingPromoResults = ref(false);
  const pendingResults = computed(
    () => pendingPromoResults.value || pendingSearchResults.value
  );
  const awake = ref(false);
  const timer = ref<NodeJS.Timeout>();
  const retryAttempts = 3;
  const _retryAfter = 1500;
  const _currentAttempt = 0;
  const retryAfter = ref(_retryAfter);
  const currentAttempt = ref(_currentAttempt);
  const requestError = ref<string | null>(null);

  const { data: ping, error: pingError } = useLazyFetch<messageT>(
    server + '/ping',
    {
      method: 'get',
      watch: false,
      server: false,
      pick: ['status_code', 'details'],
      retry: retryAttempts,
      onRequestError: exponentialBackoff,
      onResponseError: exponentialBackoff
    }
  );

  onMounted(() => {
    const mediumScreen = window.matchMedia('(max-width: 767px)').matches;
    const smallScreen = window.matchMedia('(max-width: 639px)').matches;
    if (smallScreen || touchDevice.value) _batchSize.value = 15;
    else if (mediumScreen) _batchSize.value = 30;
  });

  watch(ping, (newVal) => {
    if (newVal !== null) {
      if (newVal.status_code !== 200) console.error(newVal.details);
      else if (!awake.value && newVal.details === 'pong') {
        awake.value = true;
        getPromoResults(optionsList);
      }
      resetAttempts();
    }
  });

  watch(pingError, (newVal) => {
    if (newVal !== null) {
      const err: Error = newVal;
      console.error('Error when pinging server:\n', { err });
      requestError.value = 'Failed to connect to server';
      resetAttempts();
    }
  });

  function exponentialBackoff(context: any) {
    if (context.response !== undefined)
      console.info((context.response._data as messageT).details);
    retryAfter.value += retryAfter.value;
    if (currentAttempt.value < retryAttempts) {
      console.info(`Retrying after ${retryAfter.value / 1000} seconds`);
      context.options.retryDelay = retryAfter.value;
      currentAttempt.value++;
    }
  }

  function resetAttempts() {
    retryAfter.value = _retryAfter;
    currentAttempt.value = _currentAttempt;
  }

  async function getPromoResults(promoParams: optionsArrayT) {
    if (pendingResults.value) {
      console.info('A request is already being processed.');
      return;
    }
    requestError.value = null;
    try {
      let x = 0;
      clearInterval(timer.value);
      timer.value = setInterval(
        () => console.log(`Elapsed Time: ${++x}`),
        1000
      );
      pendingPromoResults.value = true;
      const { data, error } = await useLazyFetch<resultTemplate | messageT>(
        server + '/promo',
        {
          method: 'post',
          watch: false,
          server: false,
          body: {
            promoParams
          },
          retry: retryAttempts,
          onRequestError: exponentialBackoff,
          onResponseError: exponentialBackoff
        }
      );
      clearInterval(timer.value);
      if (data.value !== null) {
        if (data.value.status_code !== 200)
          console.error((data.value as messageT).details);
        else {
          _resultType.value = 'promo';
          _searchResults.value = data.value as resultTemplate;
          if (_searchResults.value.total > 1) sortBy('category', 'least');
        }
      } else if (error.value !== null) {
        const err: Error = error.value;
        console.error('Error when retrieving promo results\n', { err });
        requestError.value = 'Failed to retrieve promo items';
      }
      pendingPromoResults.value = false;
    } catch (error) {
      console.error('Error when retrieving promo results\n', { error });
    } finally {
      resetAttempts();
    }
  }

  async function getSearchResults(
    searchString: string,
    searchParams: optionsArrayT
  ) {
    if (pendingResults.value) {
      console.info('A request is already being processed.');
      return;
    }
    requestError.value = null;
    try {
      let x = 0;
      clearInterval(timer.value);
      timer.value = setInterval(
        () => console.log(`Elapsed Time: ${++x}`),
        1000
      );
      pendingSearchResults.value = true;
      const { data, error } = await useLazyFetch<resultTemplate | messageT>(
        server + '/search',
        {
          method: 'post',
          watch: false,
          server: false,
          body: {
            searchString,
            searchParams
          },
          retry: retryAttempts,
          onRequestError: exponentialBackoff,
          onResponseError: exponentialBackoff
        }
      );
      clearInterval(timer.value);
      if (data.value !== null) {
        if (data.value.status_code !== 200)
          console.error((data.value as messageT).details);
        else {
          _resultType.value = 'search';
          _searchResults.value = data.value as resultTemplate;
          if (_searchResults.value.total > 1) sortBy('price', 'least');
        }
      } else if (error.value !== null) {
        const err: Error = error.value;
        console.error('Error when retrieving search results\n', { err });
        requestError.value = 'Failed to retrieve search results';
      }
      pendingSearchResults.value = false;
    } catch (error) {
      console.error('Error when retrieving search results\n', { error });
    } finally {
      resetAttempts();
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

  provide('api', {
    searchResults,
    resultType,
    batchSize,
    getSearchResults,
    getPromoResults
  });

  const mainContainer =
    'flex flex-col w-full h-fit self-center grow relative shadow-md ' +
    'transition dark:shadow-gray-900/50 ';
  const errorMessage =
    'mx-auto w-60 sm:w-96 md:w-[35rem] ' +
    'title text-center text-3xl leading-tight mb-14';
</script>

<template>
  <main id="main" role="main" :class="mainContainer">
    <SearchForm />
    <div class="flex h-fit w-full text-red-400">
      <p
        v-if="requestError"
        id="requestError"
        role="alert"
        :class="errorMessage"
      >
        {{ requestError }}!
      </p>
    </div>
    <ResultWindow v-if="awake && !pendingResults && !requestError" />
    <MyLoader
      v-else-if="awake && pendingResults && !requestError"
      loader-text="Loading"
    />
    <MyLoader v-else-if="!requestError" loader-text="Connecting" />
  </main>
</template>
