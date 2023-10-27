<script setup lang="ts">
  import { computed } from 'vue-demi';

  defineProps<{ size: string }>();

  const randomId = computed(() =>
    new Uint8Array(8).map(() => Math.floor(Math.random() * 256)).join('')
  );
</script>

<template>
  <svg
    class="flag-pl"
    :width="size"
    viewBox="0 0 16 10"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g :clip-path="`url(#clip0_210_32_${randomId})`">
      <path d="M16 0H0V10H16V0Z" fill="white" />
      <path d="M16 5H0V10H16V5Z" fill="#DC143C" />
    </g>
    <defs>
      <clipPath :id="`clip0_210_32_${randomId}`">
        <rect width="16" height="10" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
