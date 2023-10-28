<script setup lang="ts">
  import { ref } from 'vue-demi';
  import { repeatBlocker } from './effectUtils';

  const buttonRef = ref<HTMLButtonElement | null>(null);

  const ariaDisabled = buttonRef.value?.ariaDisabled;

  function focus() {
    buttonRef.value?.focus();
  }

  function blur() {
    buttonRef.value?.blur();
  }

  function click() {
    buttonRef.value?.click();
  }

  defineExpose({ focus, blur, click, ariaDisabled });
</script>

<template>
  <button ref="buttonRef" v-bind="$attrs" @keydown="repeatBlocker">
    <slot></slot>
  </button>
</template>
