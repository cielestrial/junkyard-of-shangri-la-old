<script setup lang="ts">
import MyFooter from '~/components/footer/MyFooter.vue';
import MyHeader from '~/components/header/MyHeader.vue';
import MyMain from '~/components/main/MyMain.vue';

const _darkTheme = ref(false);
function changeTheme() {
  _darkTheme.value = !_darkTheme.value;
}
const colorScheme =
  'transition text-black/90 bg-white border-slate-700 dark:text-white/90 dark:bg-slate-800 dark:border-slate-400 ';
const darkTheme = readonly(_darkTheme);

provide('theme', { darkTheme, changeTheme, colorScheme });

const container =
  'view-width min-view-height flex flex-col ' +
  'text-2xl leading-tight ' +
  colorScheme;

onMounted(() => {
  /*
  _darkTheme.value =
    window.localStorage.getItem('theme') === 'dark' ||
    (window.localStorage.getItem('theme') === null &&
      window.matchMedia('(prefers-color-scheme: dark)').matches)
      ? true
      : false;
  */
});

watch(_darkTheme, (newVal) => {
  if (newVal) document.documentElement.classList.add('dark');
  else document.documentElement.classList.remove('dark');
  window.localStorage.setItem('theme', newVal ? 'dark' : 'light');
});
</script>

<template>
  <div :class="container">
    <MyHeader />
    <MyMain />
    <MyFooter />
  </div>
</template>
<style></style>
