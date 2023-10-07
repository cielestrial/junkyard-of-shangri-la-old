<script setup lang="ts">
type animationList = ['fade', 'slide', 'scale', 'switch'];
defineProps<{
  name: animationList[number];
}>();

const custom_ease_in_out = 'cubic-bezier(0.38, 0, 0.64, 1)';
</script>

<template>
  <Transition type="animation" mode="out-in" :name="name">
    <slot></slot>
  </Transition>
</template>

<style>
.slide-enter-active {
  animation: slide-down 300ms ease-out both;
}
.slide-leave-active {
  animation: slide-down 300ms ease-out reverse both;
}

.scale-enter-active {
  animation: scale-down 300ms v-bind(custom_ease_in_out) reverse both;
}
.scale-leave-active {
  animation: scale-down 300ms v-bind(custom_ease_in_out) both;
}

.fade-enter-active {
  animation: fade-in 250ms v-bind(custom_ease_in_out) both;
}
.fade-leave-active {
  animation: fade-in 250ms v-bind(custom_ease_in_out) reverse both;
}

.switch-enter-active {
  animation: fade-in 50ms v-bind(custom_ease_in_out) both;
}
.switch-leave-active {
  animation: fade-in 50ms v-bind(custom_ease_in_out) reverse both;
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
