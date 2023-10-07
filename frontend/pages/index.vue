<script setup lang="ts">
import TouchContainer from '~/components/effects/TouchContainer.vue';
import MyFooter from '~/components/footer/MyFooter.vue';
import MyHeader from '~/components/header/MyHeader.vue';
import MyMain from '~/components/main/MyMain.vue';
import SkipLinks from '~/components/header/SkipLinks.vue';

export interface theme {
  darkTheme: Readonly<Ref<boolean>>;
  changeTheme: () => void;
  colorScheme: string;
}

const colorScheme =
  'transition text-black/90 bg-white border-gray-700 ' +
  'dark:text-white/90 dark:bg-gray-800 dark:border-gray-400 dark:shadow-gray-900/50 ';

const _darkTheme = ref(false);
const darkTheme = readonly(_darkTheme);

const focusColor = computed(() => (_darkTheme.value ? '#9ca3af' : '#374151'));
const activeColor = computed(() => (_darkTheme.value ? '#9ca3af' : '#9ca3af'));

const client =
  process.env.NODE_ENV === 'production' ? '' : 'http://localhost:3000';

onMounted(() => {
  if (window.location.hash !== '') window.history.pushState(null, '', client);
  const local = window.localStorage.getItem('theme');
  if (
    local === 'dark' ||
    (local === null &&
      window.matchMedia('(prefers-color-scheme: dark)').matches)
  )
    _darkTheme.value = true;
  else _darkTheme.value = false;

  checkLocalStorageSize();
});

watch(_darkTheme, (newVal) => {
  if (newVal) document.documentElement.classList.add('dark');
  else document.documentElement.classList.remove('dark');
  window.localStorage.setItem('theme', newVal ? 'dark' : 'light');
});

function changeTheme() {
  _darkTheme.value = !_darkTheme.value;
}

function checkLocalStorageSize() {
  let _lsTotal = 0;
  let _xLen = 0;
  const keys = ['theme', 'country', 'selectedOptions'];
  const output: string[] = ['\n'];
  for (let _x in localStorage) {
    if (!localStorage.hasOwnProperty(_x) || !keys.includes(_x)) {
      continue;
    }
    _xLen = (localStorage[_x].length + _x.length) * 2;
    _lsTotal += _xLen;
    output.push(_x.substring(0, 50) + '=' + (_xLen / 1024).toFixed(3) + 'KB\n');
  }
  output.push('Total=' + (_lsTotal / 1024).toFixed(3) + '/4.096KB');
  // total local storage size capacity is 5000 KB
  // cookie storage size capacity is 4.096 KB
  console.warn(output.join(''));
}

provide('theme', { darkTheme, changeTheme, colorScheme });

const container =
  'view-width min-view-height flex flex-col text-2xl/none ' + colorScheme;
</script>

<template>
  <TouchContainer :class="container">
    <SkipLinks />
    <MyHeader />
    <MyMain />
    <MyFooter />
  </TouchContainer>
</template>

<style>
:focus-visible {
  outline: v-bind(focusColor) outset 4px;
  outline-offset: 0.5px;
}

.my-focus {
  outline: v-bind(focusColor) inset 3px;
  outline-offset: 1px;
}

.my-active {
  background-color: v-bind(activeColor) !important;
  pointer-events: none !important;
}

.my-disabled {
  opacity: 0.33 !important;
  pointer-events: none !important;
}
</style>
