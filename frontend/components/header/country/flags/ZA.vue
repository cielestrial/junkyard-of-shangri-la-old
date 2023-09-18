<script setup lang="ts">
defineProps<{
  size: string;
}>();
</script>

<template>
  <svg
    class="flag-za"
    :width="size"
    viewBox="0 0 9 6"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <g clip-path="url(#clip0_210_43)">
      <mask
        id="mask0_210_43"
        style="mask-type: luminance"
        maskUnits="userSpaceOnUse"
        x="0"
        y="0"
        width="9"
        height="6"
      >
        <path d="M0 0H9V6H0V0Z" fill="white" />
      </mask>
      <g mask="url(#mask0_210_43)">
        <path d="M0 0V6H9V0H0Z" fill="#001489" />
        <path d="M0 0V3H9V0H0Z" fill="#E03C31" />
        <path d="M0 0L4.5 3L0 6M4.5 3H9Z" fill="black" />
        <path
          d="M0 0L4.5 3M4.5 3L0 6M4.5 3H9"
          stroke="white"
          stroke-width="2"
        />
        <mask
          id="mask1_210_43"
          style="mask-type: luminance"
          maskUnits="userSpaceOnUse"
          x="0"
          y="0"
          width="5"
          height="6"
        >
          <path d="M0 0L4.5 3L0 6" fill="white" />
        </mask>
        <g mask="url(#mask1_210_43)">
          <path d="M0 0L4.5 3L0 6" fill="black" />
          <path d="M0 0L4.5 3L0 6" stroke="#FFB81C" stroke-width="2" />
        </g>
        <path
          d="M0 0L4.5 3M4.5 3L0 6M4.5 3H9"
          stroke="#007749"
          stroke-width="1.2"
        />
      </g>
    </g>
    <defs>
      <clipPath id="clip0_210_43">
        <rect width="9" height="6" fill="white" />
      </clipPath>
    </defs>
  </svg>
</template>
