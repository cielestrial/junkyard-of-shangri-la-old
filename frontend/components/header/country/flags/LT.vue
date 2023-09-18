<script setup lang="ts">
defineProps<{
  size: string;
}>();
</script>

<template>
  <svg
    class="flag-lt"
    :width="size"
    viewBox="0 0 5 3"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g clip-path="url(#clip0_210_25)">
      <path d="M5 0H0V3H5V0Z" fill="#C1272D" />
      <path d="M5 0H0V2H5V0Z" fill="#006A44" />
      <path d="M5 0H0V1H5V0Z" fill="#FDB913" />
    </g>
    <defs>
      <clipPath id="clip0_210_25">
        <rect width="5" height="3" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
