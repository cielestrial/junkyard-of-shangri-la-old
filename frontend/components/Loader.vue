<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";

defineProps<{ text: string }>();

const timer = ref<NodeJS.Timeout>();
const dot = ref(1);
const dotPresets = ref([".", "..", "...", ".."]);

onMounted(() => {
  timer.value = setInterval(() => {
    dot.value %= 4;
    dot.value++;
  }, 500);
});

onUnmounted(() => clearInterval(timer.value));

const loader = "title text-[4vmin] mx-auto cursor-default box-shadow-md ";
</script>

<template>
  <span :class="loader">{{ text }}{{ dotPresets[dot - 1] }}</span>
</template>
