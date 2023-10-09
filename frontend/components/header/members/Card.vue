<script setup lang="ts">
  import MyOverlay from '~/components/effects/MyOverlay.vue';
  import { trapFocus } from '~/components/effects/effectUtils';
  import { theme } from '~/pages/index.vue';
  import BIcons from '../../icons/BIcons.vue';

  defineEmits<{ (e: 'close'): void }>();

  const { colorScheme } = inject('theme') as theme;

  const modalRef = ref<HTMLDivElement | null>(null);

  const tabList = ref<NodeListOf<Element>>();
  const tabLength = ref(-1);
  const tabIndex = ref(-1);

  onMounted(() => {
    if (modalRef.value !== null) {
      modalRef.value.focus();
      tabIndex.value = 0;
      tabList.value = modalRef.value.querySelectorAll(
        'button, input, [tabindex = "0"]'
      );
      tabLength.value = tabList.value.length;
      if (tabLength.value > 0)
        (tabList.value[tabIndex.value] as HTMLInputElement).focus();
    }
  });

  const border = 'border-4 rounded ';
  const outer = 'h-fit w-fit shadow m-auto z-20 ' + border + colorScheme;
  const inner =
    'w-60 sm:w-72 aspect-[3/4] m-2.5 relative ' + border + colorScheme;
</script>

<template>
  <MyOverlay z="z-20" invisible>
    <MyOverlay z="z-20" invisible @click="$emit('close')" />
    <div
      ref="modalRef"
      role="alertdialog"
      aria-modal="true"
      aria-label="Members"
      aria-describedby="ComingSoon"
      @keydown.esc="
        (event) => {
          $emit('close');
          event.stopImmediatePropagation();
        }
      "
      @keydown.tab="
        (event) => {
          tabIndex = trapFocus(event, tabLength, tabIndex);
          (tabList?.[tabIndex] as HTMLInputElement)?.focus();
        }
      "
      :class="outer">
      <div :class="inner">
        <div class="absolute left-0 top-0 flex h-full w-full">
          <p
            id="ComingSoon"
            class="m-auto h-fit w-fit text-center text-2xl/tight font-bold">
            Coming Soon! <span class="absolute text-xs">TM</span>
          </p>
        </div>
        <div class="h-9 text-amber-400">
          <BIcons
            icon="star-fill"
            size="2rem"
            class="absolute left-0 top-0 m-[1vmin] rotate-12 scale-y-[-1] animate-[pulse_2s_ease-in-out_1.5s_infinite]" />
          <button
            type="button"
            class="absolute right-0 top-0 m-[1vmin] h-fit w-fit rounded-full text-red-500"
            @click="$emit('close')"
            aria-label="Close">
            <BIcons
              icon="star-fill"
              size="2rem"
              class="-rotate-12 scale-[-1] animate-[pulse_2s_ease-in-out_0.25s_infinite]" />
          </button>
        </div>
        <div class="h-9 text-amber-400">
          <BIcons
            icon="star-fill"
            size="2rem"
            class="absolute bottom-0 left-0 m-[1vmin] -rotate-12 animate-[pulse_2s_ease-in-out_0.5s_infinite]" />
          <BIcons
            icon="star-fill"
            size="2rem"
            class="absolute bottom-0 right-0 m-[1vmin] rotate-12 scale-x-[-1] animate-[pulse_2s_ease-in-out_1s_infinite]" />
        </div>
      </div>
    </div>
  </MyOverlay>
</template>
