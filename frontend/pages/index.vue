<script setup lang="ts">
  import {
    type Ref,
    computed,
    onMounted,
    provide,
    readonly,
    ref,
    watch
  } from 'vue-demi';
  import { useCookie } from 'nuxt/app';
  import { useHead } from '@unhead/vue';
  import TouchContainer from '~/components/effects/TouchContainer.vue';
  import { cookieOptions } from '~/components/effects/effectUtils';
  import MyFooter from '~/components/footer/MyFooter.vue';
  import MyHeader from '~/components/header/MyHeader.vue';
  import MyMain from '~/components/main/MyMain.vue';
  import CookieBanner from '~/components/body/CookieBanner.vue';
  import SkipLinks from '~/components/body/SkipLinks.vue';
  import Obitron from '~/assets/fonts/Orbitron-VariableFont_wght.woff2';
  import LatoRegular from '~/assets/fonts/Lato-Regular.woff2';
  import LatoBold from '~/assets/fonts/Lato-Bold.woff2';

  export type theme = {
    darkTheme: Readonly<Ref<boolean>>;
    changeTheme: () => void;
    colorScheme: string;
  };

  export type consent = {
    setConsentCookie: (newVal: boolean) => void;
    hasConsent: Readonly<Ref<boolean>>;
  };

  const consentCookie = useCookie<any>('consent', cookieOptions);
  const _hasConsent = computed(
    () => consentCookie.value !== null && consentCookie.value === true
  );
  function setConsentCookie(newVal: boolean) {
    consentCookie.value = newVal;
  }
  const hasConsent = readonly(_hasConsent);
  provide('consent', { setConsentCookie, hasConsent });

  const _darkTheme = ref(false);
  const themeCookie = useCookie<any>('theme', cookieOptions);

  if (
    hasConsent.value &&
    themeCookie.value !== null &&
    themeCookie.value === 'dark'
  )
    _darkTheme.value = true;

  useHead({
    htmlAttrs: {
      lang: 'en'
    },
    link: [
      {
        rel: 'preload',
        href: Obitron,
        crossorigin: '',
        as: 'font',
        type: 'font/woff2'
      },
      {
        rel: 'preload',
        href: LatoRegular,
        crossorigin: '',
        as: 'font',
        type: 'font/woff2'
      },
      {
        rel: 'preload',
        href: LatoBold,
        crossorigin: '',
        as: 'font',
        type: 'font/woff2'
      }
    ],
    script: [
      {
        children: `
      if (${_darkTheme.value})
        document.documentElement.classList.add('dark');
      else document.documentElement.classList.remove('dark');
        `,
        type: 'module'
      }
    ]
  });

  const colorScheme =
    'transition text-black/90 bg-white border-gray-700 ' +
    'dark:text-white/90 dark:bg-gray-800 dark:border-gray-400 dark:shadow-gray-900/50 ';
  const darkTheme = readonly(_darkTheme);
  const focusColor = computed(() => (_darkTheme.value ? '#9ca3af' : '#374151'));
  const activeColor = computed(() =>
    _darkTheme.value ? '#374151' : '#9ca3af'
  );

  onMounted(() => {
    if (window.location.hash !== '')
      window.history.pushState(null, '', window.location.origin);
    const systemThemePref = window.matchMedia(
      '(prefers-color-scheme: dark)'
    ).matches;
    if (!hasConsent.value || themeCookie.value === null)
      _darkTheme.value = systemThemePref;
    checkCookieSize();
    checkLocalStorageSize();
  });

  watch(_darkTheme, (newVal) => {
    if (newVal) {
      document.documentElement.classList.add('dark');
      if (hasConsent.value) themeCookie.value = 'dark';
    } else {
      document.documentElement.classList.remove('dark');
      if (hasConsent.value) themeCookie.value = 'light';
    }
  });

  function changeTheme() {
    _darkTheme.value = !_darkTheme.value;
  }

  provide('theme', { darkTheme, changeTheme, colorScheme });

  function checkLocalStorageSize() {
    const keys = ['theme', 'country', 'selectedOptions', 'consent'];
    const output: string[] = ['LocalStorage:\n'];
    let total = 0;
    for (let i = 0, l = localStorage.length, key, len; i < l; i++) {
      key = localStorage.key(i);
      if (key === null || !keys.includes(key)) continue;
      len = (localStorage[key].length + key.length) * 2;
      total += len;
      output.push(
        key.substring(0, 50) + '=' + (len / 1024).toFixed(3) + 'KB\n'
      );
    }
    // total local storage size capacity is 5000 KB
    output.push('Total=' + (total / 1024).toFixed(3) + '/5000KB');
    console.info(output.join(''));
  }

  function checkCookieSize() {
    // const keys = ['darkTheme', 'country', 'selectedOptions'];
    const output: string[] = ['Cookie:\n'];
    const cookie = document.cookie;
    const splitCookie = cookie.split(/=|; ?/);
    let total = 0;
    const splitLen = splitCookie.length;
    if (splitLen % 2 === 0) {
      for (let i = 0, key, len; i < splitLen; i += 2) {
        key = splitCookie[i];
        // The 1 is the '='.length
        len = (key.length + 1 + splitCookie[i + 1].length) * 2;
        total += len;
        output.push(
          key.substring(0, 50) + '=' + (len / 1024).toFixed(3) + 'KB\n'
        );
      }
    }
    // cookie storage size capacity is 4.096 KB
    output.push('Total=' + (total / 1024).toFixed(3) + '/4.096KB');
    console.info(output.join(''));
  }

  const container =
    'w-screen min-h-screen h-max flex flex-col text-2xl leading-none ' +
    colorScheme;
</script>

<template>
  <TouchContainer id="container" :class="container">
    <SkipLinks to="Main" />
    <CookieBanner />
    <MyHeader />
    <MyMain />
    <MyFooter />
  </TouchContainer>
</template>

<style>
  :focus-visible {
    outline: v-bind(focusColor) outset 4px !important;
    outline-offset: 2px !important;
  }

  .my-focus {
    outline: v-bind(focusColor) solid 4px !important;
    outline-offset: -4px !important;
  }

  .my-active {
    background-color: v-bind(activeColor) !important;
    opacity: 0.66 !important;
    pointer-events: none !important;
  }

  .my-disabled {
    opacity: 0.33 !important;
    pointer-events: none !important;
  }
</style>
