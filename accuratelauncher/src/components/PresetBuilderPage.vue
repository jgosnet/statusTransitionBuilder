<template lang="pug">
v-container(fluid).border-solid
  v-row
    v-col(cols="6")
      WoPresetConfiguration
    v-spacer
    v-col(cols="6").py-0.pl-0
      v-tabs(v-model="selectedTab" selected-class="selected-tab").my-0.py-0
        v-tab(value="providerData") Provider Data
        v-tab(value="rallyConfig" ) Rally Config

      v-window.left-align(v-model="selectedTab")
        ProviderData
        RallyConfig

</template>

<script>
import {mapGetters} from "vuex";
import { json } from '@codemirror/lang-json'
import ProviderData from "@/components/Presets/WO/ProviderData";
import RallyConfig from "@/components/Presets/WO/RallyConfig";
import WoPresetConfiguration from "@/components/Presets/WO/WoPresetConfiguration";

export default {
  name: "PresetBuilderPage",
  components: {
    WoPresetConfiguration,
    RallyConfig,
    ProviderData,
  },
  data(){
    return {
      selectedTab: 'providerData',
      expandDepth: 5,
      stringOutput: "test123",
      lang: json(),
    }
  },
  methods: {
  },
  computed: {
    ...mapGetters('woPreset', [
      "woProviderData",
      "woRallyConfig"
    ]),
  }
}
</script>

<style scoped>
.active {
       color: #222222 !important;
       background-color: #ffff !important;
    }

.selected-tab{
  background-color: ghostwhite;
}

.light-border{
  border-width: 2px;
  border-style: dashed;
}

.CodeMirror {
  border: 1px solid #eee;
  min-height: 300px;
  max-height: 300px;
  text-align: left;
  margin-bottom: 10px;
}

</style>