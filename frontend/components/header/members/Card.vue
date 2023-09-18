<script setup lang="ts">
import { computed, inject } from "vue";
import { theme } from "~/pages/index.vue";
import BIcons from "../../icons/BIcons.vue";
import Overlay from "../../Overlay.vue";

const { colorScheme } = inject("theme") as theme;

const border = "border-4 rounded box-content ";
const outer = computed(
  () => "h-fit w-fit drop-shadow-2xl m-auto " + border + colorScheme.value
);
const inner = computed(
  () =>
    "h-[40vmin] aspect-[3/4] m-[1vmin] relative " + border + colorScheme.value
);
</script>

<template>
  <Overlay>
    <Overlay @click="$emit('close')" />
    <div :class="outer">
      <div :class="inner">
        <div class="absolute top-0 left-0 h-full w-full flex">
          <h2 class="text text-center w-fit h-fit m-auto underline">
            Coming Soon!
          </h2>
        </div>
        <div class="h-9 text-amber-400">
          <BIcons
            icon="star-fill"
            size="2rem"
            class="absolute m-[1vmin] scale-y-[-1] rotate-12 top-0 left-0 animate-[pulse_2s_ease-in-out_1.5s_infinite]"
          />
          <button
            type="button"
            class="w-fit h-fit text-red-500 cursor-pointer"
            @click="$emit('close')"
          >
            <BIcons
              icon="star-fill"
              size="2rem"
              class="absolute m-[1vmin] scale-[-1] -rotate-12 top-0 right-0 animate-[pulse_2s_ease-in-out_0.25s_infinite]"
            />
          </button>
        </div>
        <div class="h-9 text-amber-400">
          <BIcons
            icon="star-fill"
            size="2rem"
            class="absolute m-[1vmin] -rotate-12 bottom-0 left-0 animate-[pulse_2s_ease-in-out_0.5s_infinite]"
          />
          <BIcons
            icon="star-fill"
            size="2rem"
            class="absolute m-[1vmin] scale-x-[-1] rotate-12 bottom-0 right-0 animate-[pulse_2s_ease-in-out_1s_infinite]"
          />
        </div>
      </div>
    </div>
  </Overlay>
</template>
