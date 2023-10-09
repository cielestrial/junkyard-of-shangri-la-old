<script setup lang="ts">
  defineProps<{
    size: string;
  }>();
</script>

<template>
  <svg
    class="flag-fr"
    :width="size"
    viewBox="0 0 3 2"
    fill="none"
    xmlns="http://www.w3.org/2000/svg">
    <g clip-path="url(#clip0_210_10)">
      <path d="M0 0H3V2H0V0Z" fill="#ED2939" />
      <path d="M0 0H2V2H0V0Z" fill="white" />
      <path d="M0 0H1V2H0V0Z" fill="#002395" />
    </g>
    <defs>
      <clipPath id="clip0_210_10">
        <rect width="3" height="2" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
