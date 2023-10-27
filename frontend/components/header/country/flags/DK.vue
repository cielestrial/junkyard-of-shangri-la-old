<script setup lang="ts">
  import { computed } from 'vue-demi';

  defineProps<{ size: string }>();

  const randomId = computed(() =>
    new Uint8Array(8).map(() => Math.floor(Math.random() * 256)).join('')
  );
</script>

<template>
  <svg
    class="flag-dk"
    :width="size"
    viewBox="0 0 370 280"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g :clip-path="`url(#clip0_210_6_${randomId})`">
      <path d="M370 0H0V280H370V0Z" fill="#C60C30" />
      <path d="M160 0H120V280H160V0Z" fill="white" />
      <path d="M370 120H0V160H370V120Z" fill="white" />
    </g>
    <defs>
      <clipPath :id="`clip0_210_6_${randomId}`">
        <rect width="370" height="280" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
