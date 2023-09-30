<template lang="pug">
v-container(fluid)
  v-row
    v-col(cols="6")
      LauncherPresetConfiguration
    v-spacer
    v-col(cols="6").py-0.pl-0
      v-tabs(v-model="selectedTab" selected-class="selected-tab").my-0.py-0
        v-tab(value="providerData") Provider Data

      v-window.left-align(v-model="selectedTab")
        LauncherPresetProviderData

</template>

<script>

import {json} from "@codemirror/lang-json";
import LauncherPresetConfiguration from "@/components/Presets/Launcher/LauncherPresetConfiguration";
import LauncherPresetProviderData from "@/components/Presets/Launcher/LauncherPresetProviderData";

export default {
  name: "LauncherPreset",
    components: {
      LauncherPresetProviderData,
      LauncherPresetConfiguration

  },
  data(){
    return {
      selectedTab: 'providerData',
      expandDepth: 5,
      stringOutput: "",
      lang: json(),
    }
  },
  methods: {
  },
  computed: {

  }
}
</script>

<style scoped>

</style>