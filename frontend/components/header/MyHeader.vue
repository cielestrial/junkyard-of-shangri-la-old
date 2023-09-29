<script setup lang="ts">
import Members from './members/Members.vue';
import MySwitch from './MySwitch.vue';
import Country from './country/Country.vue';

const nav =
  'w-full h-fit flex justify-end px-10 py-2.5 select-none ' +
  'transition shadow-md border-b-2 z-10 border-slate-200 ' +
  'dark:border-slate-700 ';

const title =
  'title w-fit h-fit text-center text-8xl my-10 ' +
  'cursor-default mx-auto z-0 ';
</script>

<template>
  <header class="flex flex-col w-full h-fit self-start">
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
