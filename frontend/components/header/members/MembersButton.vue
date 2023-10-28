<script setup lang="ts">
  import { ref } from 'vue-demi';
  import BIcons from '../../icons/BIcons.vue';
  import MyCard from './MyCard.vue';
  import MyAnimations from '~/components/effects/MyAnimations.vue';
  import MyOverlay from '~/components/effects/MyOverlay.vue';
  import MyButton from '~/components/effects/MyButton.vue';

  const membersRef = ref<InstanceType<typeof MyButton> | null>(null);
  const opened = ref(false);

  const styling =
    'w-fit h-fit py-1.5 flex text-yellow-700 transition rounded ' +
    'dark:text-yellow-500 active:scale-95 hover:animate-pulse ';
</script>
<template>
  <div>
    <MyAnimations name="fade">
      <MyOverlay v-if="opened" z="z-30" />
    </MyAnimations>
    <MyAnimations name="scale">
      <MyCard
        v-if="opened"
        @close="
          () => {
            opened = false;
            membersRef?.focus();
          }
        "
      />
    </MyAnimations>

    <MyButton
      ref="membersRef"
      type="button"
      :class="styling"
      @click="opened = !opened"
    >
      <BIcons icon="stars" size="1rem" class="-rotate-12 self-end" />
      <span class="self-center px-0.5 font-bold">Members</span>
      <BIcons
        icon="stars"
        size="1rem"
        class="rotate-12 scale-x-[-1] self-end"
      />
    </MyButton>
  </div>
</template>
