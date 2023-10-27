<script setup lang="ts">
  import { computed } from 'vue-demi';

  defineProps<{ size: string }>();

  const randomId = computed(() =>
    new Uint8Array(8).map(() => Math.floor(Math.random() * 256)).join('')
  );
</script>

<template>
  <svg
    class="flag-uk"
    :width="size"
    viewBox="0 0 60 30"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g :clip-path="`url(#clip0_208_654_${randomId})`">
      <mask
        id="mask0_208_654"
        style="mask-type: luminance"
        maskUnits="userSpaceOnUse"
        x="0"
        y="0"
        width="60"
        height="30"
      >
        <path d="M0 0V30H60V0H0Z" fill="white" />
      </mask>
      <g mask="url(#mask0_208_654)">
        <path d="M0 0V30H60V0H0Z" fill="#012169" />
        <path d="M0 0L60 30ZM60 0L0 30Z" fill="black" />
        <path d="M0 0L60 30M60 0L0 30" stroke="white" stroke-width="6" />
        <mask
          id="mask1_208_654"
          style="mask-type: luminance"
          maskUnits="userSpaceOnUse"
          x="0"
          y="0"
          width="60"
          height="30"
        >
          <path
            d="M30 15H60V30L30 15ZM30 15V30H0L30 15ZM30 15H0V0L30 15ZM30 15V0H60L30 15Z"
            fill="white"
          />
        </mask>
        <g mask="url(#mask1_208_654)">
          <path d="M0 0L60 30ZM60 0L0 30Z" fill="black" />
          <path d="M0 0L60 30M60 0L0 30" stroke="#C8102E" stroke-width="4" />
        </g>
        <path d="M30 0V30ZM0 15H60Z" fill="black" />
        <path d="M30 0V30M0 15H60" stroke="white" stroke-width="10" />
        <path d="M30 0V30ZM0 15H60Z" fill="black" />
        <path d="M30 0V30M0 15H60" stroke="#C8102E" stroke-width="6" />
      </g>
    </g>
    <defs>
      <clipPath :id="`clip0_208_654_${randomId}`">
        <rect width="60" height="30" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
