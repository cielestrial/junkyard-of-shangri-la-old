<script setup lang="ts">
  import { inject, ref, onMounted } from 'vue-demi';
  import MyAnimations from '../effects/MyAnimations.vue';
  import MyButton from '../effects/MyButton.vue';
  import type { consent, theme } from '~/pages/index.vue';

  const { colorScheme } = inject('theme') as theme;
  const { hasConsent, setConsentCookie } = inject('consent') as consent;

  const showBanner = ref(false);

  onMounted(() => {
    if (!hasConsent.value) showBanner.value = true;
  });

  function giveConsent() {
    showBanner.value = false;
    setConsentCookie(true);
  }

  const banner =
    'w-full h-fit border-2 fixed bottom-0 left-0 z-20 shadow ' + colorScheme;
  const content =
    'w-full h-fit max-h-screen flex flex-col sm:flex-row flex-nowrap gap-3 p-4 ' +
    'text-lg leading-normal overflow-y-auto ';
  const acceptButton =
    'm-auto whitespace-nowrap rounded px-2 py-1.5 font-bold transition ' +
    'text-black/90 border-2 border-gray-700 bg-green-500/90 hover:bg-green-600/90 ' +
    'dark:border-gray-800 dark:bg-green-500/90 dark:hover:bg-green-400/90 ' +
    'shadow active:scale-95 dark:shadow-gray-900/50 ';
</script>

<template>
  <MyAnimations name="slide-up" appear>
    <div v-if="showBanner" role="alert" :class="banner">
      <div :class="content">
        <p class="m-auto">
          This website uses cookies to deliver a more personalized user
          experience.
          <br />
          The only types of cookies used are strictly necessary.
          <br />
          By interacting with this site, you agree to the use of cookies.
        </p>
        <MyButton type="button" :class="acceptButton" @click="giveConsent">
          Accept
        </MyButton>
      </div>
    </div>
  </MyAnimations>
</template>
