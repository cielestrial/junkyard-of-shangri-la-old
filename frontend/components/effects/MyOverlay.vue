<script setup lang="ts">
  type zIndex = ['z-10', 'z-20', 'z-30', 'z-40', 'z-50'];

  defineProps<{
    z: zIndex[number];
    invisible?: boolean;
  }>();

  defineEmits<{ (e: 'close'): void }>();

  const overlay = 'fixed flex grow w-full h-full top-0 left-0 cursor-default ';
</script>

<template>
  <div
    type="button"
    :class="[overlay, z, { 'bg-gray-800/50': !invisible }]"
    @close="$emit('close')"
  >
    <slot></slot>
  </div>
</template>
