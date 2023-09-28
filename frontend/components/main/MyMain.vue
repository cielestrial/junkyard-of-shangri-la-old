<script setup lang="ts">
import axios, { AxiosError } from "axios";
import {
  Ref,
  computed,
  inject,
  provide,
  readonly,
  ref,
  watchEffect,
} from "vue";
import { theme } from "~/pages/index.vue";
import Loader from "../Loader.vue";
import ResultWindow from "./ResultWindow.vue";
import Search from "./Search.vue";
import { optionsArrayT } from "./optionsList";

export interface api {
  searchResults: Readonly<Ref<readonly resultTemplate[]>>;
  getSearchResults: (
    searchString: string,
    optionsList: optionsArrayT
  ) => Promise<void>;
}
interface resultTemplate {
  image: string;
  name: string;
  price: string;
  status: string;
  link: string;
}

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:3000/",
});
const server = "/api";
const { darkTheme } = inject("theme") as theme;

const _searchResults = ref<resultTemplate[]>([] as resultTemplate[]);
const searchResults = readonly(_searchResults);
const awake = ref(false);

watchEffect(async () => {
  try {
    if (!awake.value) {
      const res = await axiosInstance.get(server + "/ping");
      console.log(res.data);
      const pong = (res.data as { message: string }).message;
      if (pong === "pong") awake.value = true;
    }
  } catch (error) {
    if (axios.isAxiosError(error))
      console.log("Axios error when trying to ping server\n", { error });
    else
      console.log("Something went wrong when trying to ping server\n", error);
  }
});

async function getSearchResults(
  searchString: string,
  optionsList: optionsArrayT
) {
  try {
    const res = await axios.post(server + "/search", {
      searchString,
      optionsList,
    });
    const data = res.data;
    _searchResults.value = data as resultTemplate[];
  } catch (error) {
    console.log("Something went wrong with getSearchResults()\n", error);
  }
}

provide("api", { searchResults, getSearchResults });

const mainContainer = computed(
  () =>
    "flex flex-col w-full h-fit self-center grow border-b-2 relative shadow-md " +
    (darkTheme.value ? "border-slate-700 " : "border-slate-200 ")
);
</script>

<template>
  <main :class="mainContainer">
    <Search />
    <ResultWindow v-if="awake" />
    <Loader v-else text="Connecting" />
  </main>
</template>
