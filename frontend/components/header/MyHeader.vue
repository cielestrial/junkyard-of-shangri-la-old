<script setup lang="ts">
import CollapsedNav from './CollapsedNav.vue';
import MySwitch from './MySwitch.vue';
import Country from './country/Country.vue';
import Members from './members/Members.vue';

const nav =
  'w-full h-16 flex py-3 justify-end select-none z-10 ' +
  'transition shadow-md dark:shadow-gray-900/50 ';

const title =
  'title w-fit h-fit text-center cursor-default mx-auto z-0 my-10 ' +
  'text-4xl/tight sm:text-6xl/none md:text-8xl/none ';
</script>

<template>
  <div class="flex flex-col w-full h-fit self-start">
    <!-- or <section role="region"> -->
    <aside role="complementary" aria-label="Settings" :class="nav">
      <div
        id="settingsBar"
        class="hidden sm:flex gap-x-8 mx-10 justify-center items-end"
      >
        <Members />
        <MySwitch />
        <Country />
      </div>
      <CollapsedNav class="block sm:hidden" />
    </aside>
    <header role="banner">
      <h1 :class="title">
        Junkyard of
        <br />
        Shangri-La
      </h1>
    </header>
  </div>
</template>
