<script setup lang="ts">
import Members from "./members/Members.vue";
import MySwitch from "./MySwitch.vue";
import Country from "./country/Country.vue";
import { theme } from "~/pages/index.vue";
import { inject, computed } from "vue";

const { darkTheme } = inject("theme") as theme;
const nav = computed(
  () =>
    "w-full h-20 flex justify-end pr-10 pt-5 drop-shadow " +
    "transition transform-gpu select-none " +
    (darkTheme.value
      ? "border-b-2 border-slate-700 pb-[0.69rem] "
      : "border-b border-slate-100 pb-[0.75rem] ")
);
const title = computed(
  () =>
    "title w-fit h-fit text-[2.5vw] font-semibold cursor-default mx-auto my-10 " +
    "bg-transparent transition transform-gpu " +
    (darkTheme.value ? "text-white " : "text-black ")
);
</script>
<template>
  <header class="flex flex-col w-full">
    <!--title, members, switch, country-->
    <div :class="nav">
      <div class="flex items-center justify-between min-w-[28rem]">
        <Members />
        <MySwitch />
        <Country />
      </div>
    </div>
    <div class="w-full">
      <h1 :class="title">Junkyard of Shangri-La</h1>
    </div>
  </header>
</template>
