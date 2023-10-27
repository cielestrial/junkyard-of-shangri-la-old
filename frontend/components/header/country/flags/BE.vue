<script setup lang="ts">
  import { computed } from 'vue-demi';

  defineProps<{ size: string }>();

  const randomId = computed(() =>
    new Uint8Array(8).map(() => Math.floor(Math.random() * 256)).join('')
  );
</script>

<template>
  <svg
    class="flag-be"
    :width="size"
    viewBox="0 0 450 390"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g :clip-path="`url(#clip0_210_2_${randomId})`">
      <path d="M450 0H0V390H450V0Z" fill="#ED2939" />
      <path d="M300 0H0V390H300V0Z" fill="#FAE042" />
      <path d="M150 0H0V390H150V0Z" fill="black" />
    </g>
    <defs>
      <clipPath :id="`clip0_210_2_${randomId}`">
        <rect width="450" height="390" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
