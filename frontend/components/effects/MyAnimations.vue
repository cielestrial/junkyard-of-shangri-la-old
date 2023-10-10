<script setup lang="ts">
  type animationList = [
    'fade',
    'slide-down',
    'slide-up',
    'slide-left',
    'scale',
    'switch'
  ];
  defineProps<{
    name: animationList[number];
    appear?: boolean;
  }>();

  const customEaseInOut = 'cubic-bezier(0.38, 0, 0.64, 1)';
</script>

<template>
  <Transition type="animation" mode="out-in" :name="name" :appear="appear">
    <slot></slot>
  </Transition>
</template>

<style>
  .slide-down-enter-active {
    animation: slide-down 300ms ease-out both;
  }
  .slide-down-leave-active {
    animation: slide-down 300ms ease-out reverse both;
  }

  .slide-up-enter-active {
    animation: slide-up 300ms ease-out both;
  }
  .slide-up-leave-active {
    animation: slide-up 300ms ease-out reverse both;
  }

  .slide-left-enter-active {
    animation: slide-left 300ms ease-out both;
  }
  .slide-left-leave-active {
    animation: slide-left 300ms ease-out reverse both;
  }

  .scale-enter-active {
    animation: scale-down 300ms v-bind(customEaseInOut) reverse both;
  }
  .scale-leave-active {
    animation: scale-down 300ms v-bind(customEaseInOut) both;
  }

  .fade-enter-active {
    animation: fade-in 250ms v-bind(customEaseInOut) both;
  }
  .fade-leave-active {
    animation: fade-in 250ms v-bind(customEaseInOut) reverse both;
  }

  .switch-enter-active {
    animation: fade-in 50ms v-bind(customEaseInOut) both;
  }
  .switch-leave-active {
    animation: fade-in 50ms v-bind(customEaseInOut) reverse both;
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
  @keyframes slide-up {
    0% {
      opacity: 0;
      transform: translate3d(0, 20%, 0);
    }
    100% {
      opacity: 1;
      transform: translate3d(0, 0, 0);
    }
  }
  @keyframes slide-left {
    0% {
      position: fixed;
      opacity: 0;
      transform: translate3d(20%, 0, 0);
    }
    100% {
      position: absolute;
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
