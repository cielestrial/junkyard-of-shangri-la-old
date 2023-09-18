<script setup lang="ts">
import { ref } from "vue";
import BIcons from "../../icons/BIcons.vue";
import Card from "./Card.vue";
import MyAnimations from "../../MyAnimations.vue";

const opened = ref(false);

const styling =
  "w-fit h-fit flex flex-row text-yellow-500 drop-shadow text " +
  "active:scale-95 active:text-amber-500 active:underline cursor-pointer " +
  "hover:text-amber-400 hover:underline transition transform-gpu " +
  "focus-visible:text-amber-400 focus-visible:underline hover:animate-pulse ";
</script>
<template>
  <div>
    <MyAnimations name="scale">
      <Card v-if="opened" @close="opened = false" />
    </MyAnimations>

    <button type="button" :class="styling" @click="opened = !opened">
      <BIcons icon="stars" size="1rem" class="align-middle -rotate-12 mt-1.5" />
      <h3 class="mx-0.5 self-start">Members</h3>
      <BIcons
        icon="stars"
        size="1rem"
        class="align-middle scale-x-[-1] rotate-12 mt-1.5"
      />
    </button>
  </div>
</template>
