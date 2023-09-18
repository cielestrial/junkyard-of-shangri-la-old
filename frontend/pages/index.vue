<script setup lang="ts">
import { Ref, computed, provide, readonly, ref } from "vue";
import MyFooter from "~/components/footer/MyFooter.vue";
import MyHeader from "~/components/header/MyHeader.vue";
import MyMain from "~/components/main/MyMain.vue";
import "../css/index.css";

const _darkTheme = ref(false);
function changeTheme() {
  _darkTheme.value = !_darkTheme.value;
}
const dark = "dark text-white bg-slate-800 border-slate-400 ";
const light = "light text-black bg-white border-slate-700 ";
const _colorScheme = computed(() => (darkTheme.value ? dark : light));
const colorScheme = readonly(_colorScheme);
const darkTheme = readonly(_darkTheme);

provide("theme", { darkTheme, changeTheme, colorScheme });
export type theme = {
  darkTheme: Readonly<Ref<boolean>>;
  changeTheme: () => void;
  colorScheme: Readonly<Ref<typeof _colorScheme>>;
};
const container = computed(
  () =>
    "text-[4vmin] sm:text-[3vmin] view-width view-height transition duration-200 " +
    "transform-gpu flex flex-col " +
    colorScheme.value
);
</script>
<template>
  <div :class="container">
    <MyFooter />
    <MyMain />
    <MyHeader />
  </div>
</template>
<style></style>
