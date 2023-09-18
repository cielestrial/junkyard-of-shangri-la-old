<script setup lang="ts">
import { computed, inject, ref } from "vue";
import BIcons from "../icons/BIcons.vue";
import { theme } from "~/pages/index.vue";

const { darkTheme, changeTheme } = inject("theme") as theme;
const switchRef = ref<HTMLDivElement | null>(null);
const outer = computed(
  () =>
    "flex flex-row border-4 rounded-full w-14 h-8 px-0.5 content-center " +
    "cursor-pointer drop-shadow box-content transition transform-gpu " +
    (darkTheme.value ? "bg-slate-900 " : "bg-sky-400 ")
);
const inner = computed(
  () =>
    " rounded-full w-6 h-6 flex flex-row my-auto transition transform-gpu " +
    " fill-current drop-shadow border-2 box-content " +
    (darkTheme.value
      ? "text-white bg-sky-400 translate-x-[105%] "
      : "text-black bg-white ")
);
function toggle() {
  switchRef.value?.blur();
  changeTheme();
}
</script>

<template>
  <button type="button" class="w-fit h-fit">
    <div ref="switchRef" :class="outer" @click="toggle">
      <div :class="inner">
        <BIcons
          icon="moon-stars-fill"
          size="1rem"
          class="m-auto"
          v-if="darkTheme"
        />
        <BIcons icon="cloud-sun" size="1.3rem" class="m-auto" v-else />
      </div>
    </div>
  </button>
</template>
