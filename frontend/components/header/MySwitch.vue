<script setup lang="ts">
import MyAnimations from '../effects/MyAnimations.vue';
import { theme } from '~/pages/index.vue';
import BIcons from '../icons/BIcons.vue';

const { darkTheme, changeTheme } = inject('theme') as theme;
const switchRef = ref<HTMLDivElement | null>(null);
const outer =
  'relative flex border-4 rounded-full w-16 h-9 shadow-md ' +
  'transition bg-sky-300 border-slate-600 ' +
  'dark:bg-slate-900 dark:border-slate-400 ';

// Trasnslation: 0rem is the left, side 1rem is the center, and 2rem if the right side.
const inner =
  'absolute rounded-full w-6 aspect-[1] flex mt-[0.1875rem] shadow-md ' +
  'border-2 transition bg-white border-slate-700 translate-x-[0.1rem] ' +
  'dark:bg-sky-700 dark:border-slate-300 dark:translate-x-[1.9rem] ';

function toggle() {
  if (switchRef.value !== null) {
    //switchRef.value.blur();
    changeTheme();
  }
}
</script>

<template>
  <button type="button" class="w-fit h-fit">
    <div ref="switchRef" :class="outer" @click="toggle">
      <div :class="inner">
        <MyAnimations name="switch">
          <div v-if="darkTheme" class="m-auto text-white">
            <BIcons icon="moon-stars-fill" size="0.8rem" />
          </div>
          <span v-else class="m-auto text-black">
            <BIcons icon="cloud-sun" size="1.1rem" />
          </span>
        </MyAnimations>
      </div>
    </div>
  </button>
</template>
