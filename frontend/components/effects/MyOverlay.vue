<script setup lang="ts">
  type zIndex = ['z-10', 'z-20', 'z-30', 'z-40', 'z-50'];

  const props = defineProps<{
    z: zIndex[number];
    invisible?: boolean;
  }>();

  defineEmits<{ (e: 'close'): void }>();

  const overlay =
    'fixed flex grow w-full h-full top-0 left-0 ' +
    (props.invisible ? 'bg-transparent cursor-default ' : 'bg-gray-800/50 ') +
    props.z;
</script>

<template>
  <div type="button" :class="overlay" @close="$emit('close')">
    <slot></slot>
  </div>
</template>
