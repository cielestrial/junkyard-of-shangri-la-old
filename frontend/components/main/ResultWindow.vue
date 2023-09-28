<script setup lang="ts">
import { theme } from '~/pages/index.vue';
import { api } from './schemas';

const { colorScheme } = inject('theme') as theme;
const { searchResults } = inject('api') as api;

const resultWindow =
  'flex flex-col rounded w-[75vw] min-h-[80vh] h-fit mt-10 mb-14 mx-auto border-4 shadow-md ' +
  colorScheme;
</script>

<template>
  <div id="resultWindow" :class="resultWindow">
    <h3 v-if="searchResults.total >= 0" class="mx-auto my-4">
      {{ searchResults.total }} results found
    </h3>
    <ul
      v-if="searchResults.total > 0"
      class="w-full grow flex flex-wrap justify-evenly list-outside"
    >
      <li v-for="(result, key) in searchResults.results" :key="key">
        <div class="w-min h-min m-4">
          <img
            class="border border-slate-400"
            :src="result.image"
            :alt="'Image of ' + result.name"
          />
          <p>
            <b>{{ key + 1 }}. {{ result.name }}</b>
          </p>
          <p>{{ result.price }}</p>
          <p>{{ result.status }}</p>
          <a :href="result.link" target="_blank" rel="noreferrer noopener">
            View Product
          </a>
        </div>
      </li>
    </ul>
  </div>
</template>
