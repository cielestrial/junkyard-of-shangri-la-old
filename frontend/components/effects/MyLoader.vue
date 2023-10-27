<script setup lang="ts">
  import { onMounted, onUnmounted, ref } from 'vue-demi';

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

  const loader = 'title text-3xl leading-none mx-auto mb-14 cursor-wait ';
</script>

<template>
  <span :aria-label="loaderText" :class="loader"
    >{{ loaderText }}{{ dotPresets[dot - 1] }}</span
  >
</template>
