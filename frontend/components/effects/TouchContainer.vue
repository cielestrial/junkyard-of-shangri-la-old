<script setup lang="ts">
  const _touchDevice = ref(false);
  const touchDevice = readonly(_touchDevice);

  const touchStart = ref({ x: -1, y: -1 });
  const touchEnd = ref({ x: -1, y: -1 });
  const yDiff = computed(() => Math.abs(touchEnd.value.y - touchStart.value.y));
  const xDiff = computed(() => Math.abs(touchEnd.value.x - touchStart.value.x));

  let width: number;
  let height: number;
  let deadzoneX: number;
  let deadzoneY: number;

  let downArrowEvent: KeyboardEvent;
  let upArrowEvent: KeyboardEvent;
  let leftArrowEvent: KeyboardEvent;
  let rightArrowEvent: KeyboardEvent;

  onMounted(() => {
    width = window.outerWidth;
    height = window.outerHeight;
    deadzoneX = 0.05 * width;
    deadzoneY = 0.1 * height;

    downArrowEvent = new KeyboardEvent('keydown', { key: 'ArrowDown' });
    upArrowEvent = new KeyboardEvent('keydown', { key: 'ArrowUp' });
    leftArrowEvent = new KeyboardEvent('keydown', { key: 'ArrowLeft' });
    rightArrowEvent = new KeyboardEvent('keydown', { key: 'ArrowRight' });
  });

  function reset() {
    console.log('touch canceled');
    touchStart.value = { x: -1, y: -1 };
    touchEnd.value = { x: -1, y: -1 };
  }

  function trackTouch(event: TouchEvent) {
    console.log('touch started');
    if (!_touchDevice.value) _touchDevice.value = true;
    touchStart.value = {
      x: event.changedTouches[0].pageX,
      y: event.changedTouches[0].pageY
    };
  }

  function calculateSwipe(event: TouchEvent) {
    if (touchStart.value.x !== -1 || touchStart.value.y !== -1) {
      touchEnd.value = {
        x: event.changedTouches[0].pageX,
        y: event.changedTouches[0].pageY
      };
      if (yDiff > xDiff) {
        // swipe up
        if (touchStart.value.y > touchEnd.value.y + deadzoneY)
          document.dispatchEvent(downArrowEvent);
        // swipe down
        else if (touchStart.value.y < touchEnd.value.y - deadzoneY)
          document.dispatchEvent(upArrowEvent);
      } else if (yDiff < xDiff) {
        // swipe left
        if (touchStart.value.x > touchEnd.value.x + deadzoneX)
          document.dispatchEvent(rightArrowEvent);
        // swipe right
        else if (touchStart.value.x < touchEnd.value.x - deadzoneX)
          document.dispatchEvent(leftArrowEvent);
      }
    }
  }

  provide('touch', { touchDevice });
</script>

<template>
  <div
    @touchStart.passive="trackTouch"
    @touchEnd.passive="calculateSwipe"
    @touchCancel.passive="reset"
  >
    <slot></slot>
  </div>
</template>
