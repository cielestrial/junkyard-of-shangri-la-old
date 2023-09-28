<script setup lang="ts">
import { Ref, computed, provide, readonly, ref } from "vue";
import MyFooter from "~/components/footer/MyFooter.vue";
import MyHeader from "~/components/header/MyHeader.vue";
import MyMain from "~/components/main/MyMain.vue";

export type theme = {
  darkTheme: Readonly<Ref<boolean>>;
  changeTheme: () => void;
  colorScheme: Readonly<Ref<typeof _colorScheme>>;
};

const _darkTheme = ref(false);
function changeTheme() {
  _darkTheme.value = !_darkTheme.value;
}
const dark = "dark text-white/90 bg-slate-800 border-slate-400 transition ";
const light = "light text-black/90 bg-white border-slate-700 transition ";
const _colorScheme = computed(() => (darkTheme.value ? dark : light));
const colorScheme = readonly(_colorScheme);
const darkTheme = readonly(_darkTheme);

provide("theme", { darkTheme, changeTheme, colorScheme });

const container = computed(
  () =>
    "view-width min-view-height flex flex-col " +
    "text-[4vmin] sm:text-[3vmin] leading-none " +
    colorScheme.value
);
</script>

<template>
  <div :class="container">
    <MyHeader />
    <MyMain />
    <MyFooter />
  </div>
</template>
<style></style>
