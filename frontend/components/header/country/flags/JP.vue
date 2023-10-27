<script setup lang="ts">
  import { computed } from 'vue-demi';

  defineProps<{ size: string }>();

  const randomId = computed(() =>
    new Uint8Array(8).map(() => Math.floor(Math.random() * 256)).join('')
  );
</script>

<template>
  <svg
    class="flag-jp"
    :width="size"
    viewBox="0 0 900 600"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g :clip-path="`url(#clip0_210_22_${randomId})`">
      <path d="M900 0H0V600H900V0Z" fill="white" />
      <path
        d="M450 480C549.411 480 630 399.411 630 300C630 200.589 549.411 120 450 120C350.589 120 270 200.589 270 300C270 399.411 350.589 480 450 480Z"
        fill="#BC002D"
      />
    </g>
    <defs>
      <clipPath :id="`clip0_210_22_${randomId}`">
        <rect width="900" height="600" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
