<script setup lang="ts">
import Overlay from '~/components/effects/Overlay.vue';
import { theme } from '~/components/main/schemas';
import BIcons from '../../icons/BIcons.vue';

defineEmits<{ (e: 'close'): void }>();

const { colorScheme } = inject('theme') as theme;

const border = 'border-4 rounded ';
const outer = 'h-fit w-fit shadow-md m-auto z-20 ' + border + colorScheme;
const inner =
  'w-[40vmin] aspect-[3/4] m-[1.5vmin] relative ' + border + colorScheme;
</script>

<template>
  <Overlay z="z-20" invisible>
    <Overlay z="z-20" invisible @click="$emit('close')" />
    <div :class="outer">
      <div :class="inner">
        <div class="absolute top-0 left-0 h-full w-full flex">
          <h2 class="text-center text-2xl w-fit h-fit m-auto">
            Coming Soon! <span class="text-xs absolute">TM</span>
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
            class="w-fit h-fit text-red-500 absolute top-0 right-0 m-[1vmin]"
            @click="$emit('close')"
          >
            <BIcons
              icon="star-fill"
              size="2rem"
              class="scale-[-1] -rotate-12 animate-[pulse_2s_ease-in-out_0.25s_infinite]"
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
