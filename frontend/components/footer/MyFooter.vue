<script setup lang="ts">
import { computed, inject } from "vue";
import { theme } from "~/pages/index.vue";

const { darkTheme } = inject("theme") as theme;

const foot = computed(
  () =>
    "w-full h-fit flex mt-5 px-10 py-2.5 transition select-none border-t-2 relative z-0 " +
    (darkTheme.value
      ? "bg-slate-900 border-slate-700 "
      : "bg-sky-300 border-slate-400 ")
);
</script>
<template>
  <footer :class="foot">
    <div class="w-full h-8 my-auto text-center"></div>
  </footer>
</template>
