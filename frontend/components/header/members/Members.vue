<script setup lang="ts">
  import { ref } from 'vue';
  import MyAnimations from '~/components/effects/MyAnimations.vue';
  import MyOverlay from '~/components/effects/MyOverlay.vue';
  import BIcons from '../../icons/BIcons.vue';
  import Card from './Card.vue';

  const membersRef = ref<HTMLButtonElement | null>(null);
  const opened = ref(false);

  const styling =
    'w-fit h-fit py-1.5 flex text-yellow-500 transition rounded ' +
    'active:scale-95 active:text-amber-500 active:underline ' +
    'hover:text-amber-400 hover:underline hover:animate-pulse ' +
    'focus-visible:text-amber-400 focus-visible:underline focus:-visible:animate-pulse ' +
    'focus-visible:border-gray-700 dark:focus-visible:border-gray-400 ';
</script>
<template>
  <div>
    <Teleport to="body">
      <MyAnimations name="fade">
        <MyOverlay z="z-20" v-if="opened" />
      </MyAnimations>
      <MyAnimations name="scale">
        <Card
          v-if="opened"
          @close="
            () => {
              opened = false;
              membersRef?.focus();
            }
          " />
      </MyAnimations>
    </Teleport>

    <button
      ref="membersRef"
      type="button"
      :class="styling"
      @click="opened = !opened">
      <BIcons
        icon="stars"
        size="1rem"
        class="-rotate-12 self-end align-middle" />
      <p class="self-center px-0.5 font-bold">Members</p>
      <BIcons
        icon="stars"
        size="1rem"
        class="rotate-12 scale-x-[-1] self-end align-middle" />
    </button>
  </div>
</template>
