<script setup lang="ts">
defineProps<{ loaderText: string }>();

const timer = ref<NodeJS.Timeout>();
const dot = ref(1);
const dotPresets = ref(['.', '..', '...', '..']);

onMounted(() => {
  timer.value = setInterval(() => {
    dot.value %= 4;
    dot.value++;
  }, 500);
});

onUnmounted(() => clearInterval(timer.value));

const loader = 'title text-3xl mx-auto cursor-default ';
</script>

<template>
  <span :class="loader">{{ loaderText }}{{ dotPresets[dot - 1] }}</span>
</template>
