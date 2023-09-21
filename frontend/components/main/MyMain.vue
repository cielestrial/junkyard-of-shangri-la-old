<script setup lang="ts">
import { computed, inject } from "vue";
import { theme } from "~/pages/index.vue";

import Search from "./Search.vue";

const { colorScheme } = inject("theme") as theme;

const resultWindow = computed(
  () =>
    "rounded w-[75vw] h-[80vh] my-10 mx-auto border-4 shadow-md relative z-0 " +
    colorScheme.value
);
</script>

<template>
  <main class="flex flex-col w-full h-fit">
    <Search />
    <div id="resultWindow" :class="resultWindow"></div>
  </main>
</template>
