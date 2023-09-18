<script setup lang="ts"></script>
<template>
  <button
    type="button"
    class="fixed flex view-width view-height top-0 left-0 bg-transparent"
    @click="$emit('click')"
    @close="$emit('close')"
  >
    <slot></slot>
  </button>
</template>
