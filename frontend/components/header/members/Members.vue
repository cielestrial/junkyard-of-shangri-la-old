<script setup lang="ts">
import { ref } from "vue";
import BIcons from "../../icons/BIcons.vue";
import Card from "./Card.vue";
import MyAnimations from "../../MyAnimations.vue";
import Overlay from "~/components/Overlay.vue";

const opened = ref(false);

const styling =
  "w-fit h-fit mb-[0.3rem] flex text-yellow-500 box-shadow-md transition " +
  "active:scale-95 active:text-amber-500 active:underline " +
  "hover:text-amber-400 hover:underline hover:animate-pulse " +
  "focus-visible:text-amber-400 focus-visible:underline ";
</script>
<template>
  <div>
    <MyAnimations name="fade">
      <Overlay z="z-20" v-if="opened" />
    </MyAnimations>
    <MyAnimations name="scale">
      <Card v-if="opened" @close="opened = false" />
    </MyAnimations>

    <button type="button" :class="styling" @click="opened = !opened">
      <BIcons
        icon="stars"
        size="1rem"
        class="align-middle -rotate-12 self-end"
      />
      <h3 class="px-0.5 self-center">Members</h3>
      <BIcons
        icon="stars"
        size="1rem"
        class="align-middle scale-x-[-1] rotate-12 self-end"
      />
    </button>
  </div>
</template>
