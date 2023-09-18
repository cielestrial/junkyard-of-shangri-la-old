<script setup lang="ts">
const animationList = ["fade", "slide", "scale"] as const;
defineProps<{
  name: (typeof animationList)[number];
}>();
</script>

<template>
  <Transition type="animation" :name="name">
    <slot></slot>
  </Transition>
</template>

<style>
.slide-enter-active {
  animation: slide-down 0.2s ease-out both;
}
.slide-leave-active {
  animation: slide-up 0.2s ease-out both;
}

.scale-enter-active {
  animation: scale-down 0.34s cubic-bezier(0.38, 0, 0.64, 1) reverse both;
}
.scale-leave-active {
  animation: scale-down 0.5s cubic-bezier(0.38, 0, 0.64, 1) both;
}

.fade-in-active {
  animation: fade-in 0.67s cubic-bezier(0.38, 0, 0.64, 1) both;
}
.fade-out-active {
  animation: fade-in 0.5s cubic-bezier(0.38, 0, 0.64, 1) reverse both;
}

@keyframes slide-up {
  0% {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
  100% {
    opacity: 0;
    transform: translate3d(0, -20%, 0);
  }
}
@keyframes slide-down {
  0% {
    opacity: 0;
    transform: translate3d(0, -20%, 0);
  }
  100% {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
}
@keyframes scale-down {
  0% {
    opacity: 1;
    transform: scale3d(100%, 100%, 100%);
  }
  100% {
    opacity: 0;
    transform: scale3d(50%, 50%, 100%);
  }
}
@keyframes fade-in {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
