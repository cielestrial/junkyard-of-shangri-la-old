<script setup lang="ts">
  import { inject } from 'vue-demi';
  import BIcons from '../icons/BIcons.vue';
  import MyLogo from '../icons/MyLogo.vue';
  import { theme } from '~/pages/index.vue';

  const { colorScheme } = inject('theme') as theme;

  const footer =
    'relative z-0 h-fit w-full select-none flex flex-col gap-y-6 ' +
    'pb-8 pt-11 px-5 sm:px-10 text-lg leading-tight text-center';
  const iconSize = '2rem';
  const link = 'transition p-0.5 rounded active:scale-95 hover:animate-pulse ';
  const linkButton =
    'w-fit h-fit rounded-full flex py-2.5 px-3 gap-2 m-auto ' +
    'font-bold border-4 shadow active:scale-95 active:bg-gray-300 ' +
    'dark:active:bg-gray-600 hover:bg-gray-200 dark:hover:bg-gray-500 ' +
    'hover:animate-pulse ' +
    colorScheme;
</script>

<template>
  <footer id="footer" role="contentinfo" :class="footer">
    <!--Screen reader test this link button-->
    <a
      id="contactButton"
      aria-labelledby="contactText"
      href="https://cielestrial.github.io/#Contact"
      target="_blank"
      rel="noreferrer noopener"
      :class="linkButton"
    >
      <MyLogo class="rounded-full" :size="iconSize" />
      <span id="contactText" class="my-auto text-2xl leading-none">
        Contact
      </span>
    </a>

    <div class="my-auto w-full flex flex-wrap gap-y-7 gap-x-10 justify-evenly">
      <div class="flex my-auto gap-y-7 gap-x-10">
        <a
          aria-label="My porfolio website"
          href="https://cielestrial.github.io/#Home"
          target="_blank"
          rel="noreferrer noopener"
          :class="link"
        >
          <MyLogo class="rounded-full" :size="iconSize" />
        </a>
        <a
          aria-label="My LinkedIn profile"
          href="https://www.linkedin.com/in/boladale-ogunleye-089937186"
          target="_blank"
          rel="noreferrer noopener"
          :class="link"
        >
          <BIcons
            class="rounded text-[#0864c0] dark:text-white/90 transition"
            icon="linkedin"
            :size="iconSize"
          />
        </a>
        <a
          aria-label="My Github profile"
          href="https://github.com/cielestrial"
          target="_blank"
          rel="noreferrer noopener"
          :class="link"
        >
          <BIcons class="rounded-full" icon="github" :size="iconSize" />
        </a>
      </div>

      <div
        class="flex flex-wrap my-auto justify-center gap-y-7 gap-x-6 underline"
      >
        <a
          href="https://www.termsfeed.com/live/34ad6597-6ca3-4f3a-8124-71d952006d2f"
          target="_blank"
          rel="noreferrer noopener"
          :class="link"
        >
          Terms & Conditions
        </a>
        <a
          href="https://www.termsfeed.com/live/68e2bd3c-90d0-4e03-bc08-84b24e71065b"
          target="_blank"
          rel="noreferrer noopener"
          :class="link"
        >
          Privacy Policy
        </a>
      </div>

      <div class="my-auto p-0.5">Copyright &copy; 2023 &#124; cielestrial</div>
    </div>
  </footer>
</template>
