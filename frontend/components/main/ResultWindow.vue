<script setup lang="ts">
import { computed, inject } from "vue";
import { theme } from "~/pages/index.vue";
import { api } from "./MyMain.vue";

const { colorScheme } = inject("theme") as theme;
const { searchResults } = inject("api") as api;

const resultWindow = computed(
  () =>
    "flex flex-col rounded w-[75vw] h-[80vh] mt-10 mb-14 mx-auto border-4 shadow-md " +
    colorScheme.value
);
</script>

<template>
  <div id="resultWindow" :class="resultWindow">
    <h3 class="mx-auto my-4 mb-">{{ searchResults.length }} results found</h3>
    <ul
      v-if="searchResults.length > 0"
      class="w-full grow flex flex-wrap justify-evenly list-outside"
    >
      <li v-for="(result, key) in searchResults" :key="key">
        <div class="w-min h-min m-4">
          <img
            class="border border-slate-400"
            :src="result.image"
            :alt="'Image of ' + result.name"
          />
          <p>
            <b>{{ key }}. {{ result.name }}</b>
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
