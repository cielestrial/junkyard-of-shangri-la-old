<script setup lang="ts">
  defineProps<{
    size: string;
  }>();
</script>

<template>
  <svg
    class="flag-be"
    :width="size"
    viewBox="0 0 450 390"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g clip-path="url(#clip0_210_2)">
      <path d="M450 0H0V390H450V0Z" fill="#ED2939" />
      <path d="M300 0H0V390H300V0Z" fill="#FAE042" />
      <path d="M150 0H0V390H150V0Z" fill="black" />
    </g>
    <defs>
      <clipPath id="clip0_210_2">
        <rect width="450" height="390" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
