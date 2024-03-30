<script setup lang="ts">
  import { inject, ref, watch } from 'vue-demi';
  import MyAnimations from '../effects/MyAnimations.vue';
  import MyOverlay from '../effects/MyOverlay.vue';
  import { trapFocus } from '../effects/effectUtils';
  import BIcons from '../icons/BIcons.vue';
  import MyButton from '../effects/MyButton.vue';
  import MySwitch from './MySwitch.vue';
  import CountrySelect from './country/CountrySelect.vue';
  import MembersButton from './members/MembersButton.vue';
  import type { theme } from '~/pages/index.vue';

  const { colorScheme } = inject('theme') as theme;

  const hamburgerRef = ref<InstanceType<typeof MyButton> | null>(null);
  const modalRef = ref<HTMLDivElement | null>(null);
  const opened = ref(false);

  const tabList = ref<NodeListOf<Element>>();
  const tabLength = ref(-1);
  const tabIndex = ref(-1);

  watch(modalRef, (newVal) => {
    if (newVal !== null) {
      tabIndex.value = 0;
      tabList.value = newVal.querySelectorAll(
        'button, input, [tabindex = "0"]'
      );
      tabLength.value = tabList.value.length;
      if (tabLength.value > 0)
        (tabList.value[tabIndex.value] as HTMLInputElement).focus();
    }
  });

  function close() {
    opened.value = false;
    if (hamburgerRef.value !== null) hamburgerRef.value.focus();
  }

  const _menu = 'w-fit h-fit z-10 rounded border-2 shadow ' + colorScheme;
  const menuButton =
    _menu +
    'relative mx-5 p-2 ' +
    'active:scale-95 active:bg-gray-300 dark:active:bg-gray-600 ' +
    'hover:animate-pulse hover:bg-gray-200 dark:hover:bg-gray-500 ';
  const drawer = _menu + 'absolute right-0.5 top-0.5 z-10 ';
  const exitButton =
    'absolute top-2 right-2 ' +
    'w-fit h-fit bg-white/90 rounded active:scale-95 ' +
    'shadow dark:shadow-gray-900/50 hover:animate-pulse ' +
    'transition text-red-600 dark:text-red-400 ';
</script>

<template>
  <div>
    <MyButton
      ref="hamburgerRef"
      aria-label="Menu"
      type="button"
      :class="menuButton"
      @click="
        () => {
          opened = true;
          hamburgerRef?.focus();
        }
      "
    >
      <BIcons class="rounded-full" icon="list" size="1.5rem" />
    </MyButton>

    <MyAnimations name="fade">
      <MyOverlay v-if="opened" z="z-10" @click="close" />
    </MyAnimations>
    <MyAnimations name="slide-left">
      <div
        v-if="opened"
        id="drawer"
        ref="modalRef"
        role="dialog"
        aria-modal="true"
        aria-label="Menu"
        :class="drawer"
        @keydown.esc="
          (event) => {
            if (!event.repeat) opened = false;
            event.stopImmediatePropagation();
          }
        "
        @keydown.tab="
          (event) => {
            tabIndex = trapFocus(event, tabLength, tabIndex);
            (tabList?.[tabIndex] as HTMLInputElement)?.focus();
          }
        "
      >
        <MyButton
          aria-label="Close"
          type="button"
          :class="exitButton"
          @click="close"
        >
          <BIcons icon="x-square-fill" size="1.5rem" />
        </MyButton>

        <div class="mb-2 mt-4 flex flex-col items-center gap-y-8 p-8">
          <MembersButton />
          <MySwitch />
          <CountrySelect />
        </div>
      </div>
    </MyAnimations>
  </div>
</template>
