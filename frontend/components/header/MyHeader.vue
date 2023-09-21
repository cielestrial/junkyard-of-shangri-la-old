<script setup lang="ts">
import Members from "./members/Members.vue";
import MySwitch from "./MySwitch.vue";
import Country from "./country/Country.vue";
import { theme } from "~/pages/index.vue";
import { inject, computed } from "vue";

const { darkTheme } = inject("theme") as theme;
const nav = computed(
  () =>
    "w-full h-fit flex justify-end px-10 py-2.5 select-none " +
    "transition shadow-md border-b-2 z-10 " +
    (darkTheme.value ? "border-slate-700 " : "border-slate-200 ")
);
const title = computed(
  () =>
    "title w-fit h-fit text-center text-[15vmin] my-10 " +
    "cursor-default transition box-shadow-md mx-auto z-0 " +
    (darkTheme.value ? "text-white/90 " : "text-black/90 ")
);
</script>

<template>
  <header class="flex flex-col w-full h-fit">
    <!--title, members, switch, country-->
    <div :class="nav">
      <div class="flex items-end justify-between min-w-[28rem]">
        <Members />
        <MySwitch />
        <Country />
      </div>
    </div>
    <h1 :class="title">
      Junkyard of
      <br />
      Shangri-La
    </h1>
  </header>
</template>
