<script setup lang="ts">
type zIndex = ["z-10", "z-20", "z-30", "z-40", "z-50"];
const props = defineProps<{
  z: zIndex[number];
  invisible?: boolean;
}>();
const overlay =
  "fixed flex grow view-width view-height top-0 left-0 " +
  (props.invisible ? "bg-transparent cursor-default " : "bg-slate-800/50 ") +
  props.z;
</script>

<template>
  <div
    type="button"
    :class="overlay"
    @click="$emit('click')"
    @close="$emit('close')"
  >
    <slot></slot>
  </div>
</template>
