<script setup lang="ts">
  import { inject, ref } from 'vue-demi';
  import MyButton from '~/components/effects/MyButton.vue';
  import type { theme } from '~/pages/index.vue';

  const { colorScheme } = inject('theme') as theme;

  const backToTopRef = ref<InstanceType<typeof MyButton> | null>(null);

  function jumpToTop() {
    const element = document.getElementById('container');
    element?.scrollIntoView(true);
    backToTopRef.value?.blur();
  }

  const stickyButton =
    'z-10 sticky bottom-3 mr-3 mb-3 w-fit h-fit rounded-full py-2.5 px-3 ' +
    'font-bold border-4 shadow active:scale-95 active:bg-gray-300 ' +
    'dark:active:bg-gray-600 hover:bg-gray-200 dark:hover:bg-gray-500 ' +
    colorScheme;
</script>

<template>
  <span class="absolute w-full h-full top-0 flex flex-col">
    <span class="relative w-full grow mt-[27.5rem] flex justify-end items-end">
      <MyButton
        id="backToTop"
        ref="backToTopRef"
        type="button"
        :class="stickyButton"
        @click="jumpToTop"
      >
        Back to Top
      </MyButton>
    </span>
  </span>
</template>
