<script setup lang="ts">
  import { optionsArrayT, optionsList } from '../optionsList';
  import { options } from '../schemas';
  import MyOverlay from '~/components/effects/MyOverlay.vue';
  import { trapFocus } from '~/components/effects/effectUtils';
  import BIcons from '~/components/icons/BIcons.vue';
  import { theme } from '~/pages/index.vue';

  defineEmits<{ (e: 'close'): void }>();

  const { colorScheme } = inject('theme') as theme;
  const { selectedOptions, setSelectedOptions } = inject('options') as options;

  const modalRef = ref<HTMLDivElement | null>(null);
  const scrollRef = ref<HTMLElement | null>(null);
  const allRef = ref<HTMLInputElement | null>(null);

  const allChecked = ref(false);
  const searchOptions = ref<optionsArrayT>(optionsList);
  const optionLength = searchOptions.value.length;
  const selectedSearchOptions = ref(selectedOptions.value.slice(0));

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

  watch([selectedSearchOptions, allRef], handleAllOnChange);

  function handleAllOnChange() {
    if (allRef.value !== null) {
      const length = selectedSearchOptions.value.length;
      allChecked.value = false;
      allRef.value.indeterminate = false;
      if (length === optionLength) allChecked.value = true;
      else if (length !== 0) allRef.value.indeterminate = true;
      setSelectedOptions(selectedSearchOptions.value);
    }
  }

  function handleAllOnClick() {
    if (allRef.value !== null) {
      if (allChecked.value) selectedSearchOptions.value = [];
      else selectedSearchOptions.value = searchOptions.value;
    }
  }

  function parallelScroll(e: WheelEvent) {
    if (scrollRef.value !== null) {
      const scrollBy = Math.floor(scrollRef.value.scrollWidth * 0.1);
      if (e.deltaY > 0) scrollRef.value.scrollLeft += scrollBy;
      else if (e.deltaY < 0) scrollRef.value.scrollLeft -= scrollBy;
    }
  }

  const border = 'border-4 rounded transition ';
  const checkboxOuterArea =
    'w-fit h-fit m-auto shadow select-none z-20 ' + border + colorScheme;
  const checkboxInnerArea =
    'w-[80vmin] aspect-[1] m-2.5 px-2.5 ' + border + colorScheme;
  const exitButton =
    'w-fit h-fit text-red-500 bg-white/90 rounded self-end absolute ' +
    'shadow dark:shadow-gray-900/50 active:scale-95 ';
  const checkboxGroup =
    'flex flex-col flex-wrap w-full h-full list-outside pl-2.5 ' +
    'gap-x-2 gap-y-0.5 overflow-auto overscroll-none text-xl/normal ';
  const checkbox = 'cursor-pointer w-fit h-fit my-auto';
</script>

<template>
  <MyOverlay z="z-20" invisible>
    <MyOverlay z="z-20" invisible @click="$emit('close')" />
    <div
      ref="modalRef"
      role="dialog"
      aria-modal="true"
      aria-label="Search Options"
      :class="checkboxOuterArea"
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
      @keydown.arrow-right="scrollRef?.focus()"
      @keydown.arrow-left="scrollRef?.focus()"
    >
      <div :class="checkboxInnerArea">
        <div class="flex h-fit w-full flex-col pb-1 pt-2">
          <button
            aria-label="Close"
            type="button"
            :class="exitButton"
            @click="$emit('close')"
          >
            <BIcons icon="x-square-fill" size="1.5rem" />
          </button>
          <div class="mt-2 flex h-fit w-fit gap-x-1 self-start">
            <input
              id="all"
              ref="allRef"
              aria-controls="checkboxGroup"
              type="checkbox"
              :class="checkbox"
              :checked="allChecked"
              @change="handleAllOnClick"
            />
            <label
              for="all"
              class="cursor-pointer text-xl font-bold leading-none"
            >
              All
            </label>
          </div>
        </div>

        <ol
          id="checkboxGroup"
          ref="scrollRef"
          role="group"
          aria-label="Book Categories"
          tabindex="-1"
          :class="checkboxGroup"
          @wheel.passive="parallelScroll"
        >
          <li v-for="(option, key) in searchOptions" :key="key">
            <div class="flex gap-x-1">
              <input
                :id="option"
                v-model="selectedSearchOptions"
                type="checkbox"
                name="websites"
                :value="option"
                :class="checkbox"
              />
              <label :for="option" class="cursor-pointer whitespace-nowrap">
                {{ option }}
              </label>
            </div>
          </li>
        </ol>
      </div>
    </div>
  </MyOverlay>
</template>
