<script setup lang="ts">
  defineProps<{
    size: string;
  }>();
</script>

<template>
  <svg
    class="flag-ie"
    :width="size"
    viewBox="0 0 600 300"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g clip-path="url(#clip0_210_14)">
      <mask
        id="mask0_210_14"
        style="mask-type: luminance"
        maskUnits="userSpaceOnUse"
        x="0"
        y="0"
        width="600"
        height="300"
      >
        <path d="M600 0H0V300H600V0Z" fill="white" />
      </mask>
      <g mask="url(#mask0_210_14)">
        <path d="M200 0H0V300H200V0Z" fill="#169B62" />
        <path d="M400 0H200V300H400V0Z" fill="white" />
        <path d="M600 0H400V300H600V0Z" fill="#FF883E" />
      </g>
    </g>
    <defs>
      <clipPath id="clip0_210_14">
        <rect width="600" height="300" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
