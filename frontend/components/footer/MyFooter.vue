<script setup lang="ts">
import { computed, inject } from "vue";
import { theme } from "~/pages/index.vue";

const { darkTheme } = inject("theme") as theme;

const foot = computed(
  () =>
    "w-full h-fit flex self-end px-10 pt-6 pb-2 transition select-none " +
    "relative z-0 "
);
</script>
<template>
  <footer :class="foot">
    <div class="w-full h-8 my-auto text-center"></div>
  </footer>
</template>
