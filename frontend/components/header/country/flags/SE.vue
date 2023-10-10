<script setup lang="ts">
  defineProps<{
    size: string;
  }>();
</script>

<template>
  <svg
    class="flag-se"
    :width="size"
    viewBox="0 0 16 10"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g clip-path="url(#clip0_210_39)">
      <path d="M16 0H0V10H16V0Z" fill="#006AA7" />
      <path d="M7 0H5V10H7V0Z" fill="#FECC00" />
      <path d="M16 4H0V6H16V4Z" fill="#FECC00" />
    </g>
    <defs>
      <clipPath id="clip0_210_39">
        <rect width="16" height="10" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
