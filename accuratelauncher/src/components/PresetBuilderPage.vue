<template lang="pug">
v-container(fluid).border-solid
  v-row
    v-col(cols="6")
      | test
    v-spacer
    v-col(cols="6").light-border.py-0.pl-0
      v-tabs(v-model="selectedTab" selected-class="selected-tab").my-0.py-0
        v-tab(value="providerData") Provider Data
        v-tab(value="rallyConfig" ) Rally Config

      v-window.left-align(v-model="selectedTab")
        v-window-item(value="providerData" )
          v-row.my-1
            v-btn.mx-2.my-1(
              prepend-icon="fa-solid fa-copy"
              v-clipboard="woProviderData"
              v-clipboard:success="clipboardSuccessHandler"
              v-clipboard:error="clipboardErrorHandler"
              ) Copy
            v-alert.float-right(title="Copied to clipboard."
              type="success"
              color="success"
              density="compact"
              v-show="dismissCountDown > 0")

          v-row.mx-1
            //Codemirror(v-model="woProviderData" :lang="lang")
            CodeEditor
            //| {{woProviderData}}


        v-window-item(value="rallyConfig" )
          v-row.my-1
            v-btn.mx-2.my-1(
              prepend-icon="fa-solid fa-copy"
              v-clipboard="woRallyConfig"
              v-clipboard:success="clipboardSuccessHandler"
              v-clipboard:error="clipboardErrorHandler"
              ) Copy
            v-alert.float-right(title="Copied to clipboard."
              type="success"
              color="success"
              density="compact"
              v-show="dismissCountDown > 0")

          v-row.mx-1
            | {{woRallyConfig}}
            //code-mirror.w-100.CodeMirror(v-model="woRallyConfig"
            //  basic
            //  :lang="lang"
            //  readonly
            //gutter
            //  )
</template>

<script>
import {mapGetters} from "vuex";
import { Codemirror } from 'vue-codemirror'
import { json } from '@codemirror/lang-json'
import CodeEditor from "@/components/Presets/WO/CodeEditor";

export default {
  name: "PresetBuilderPage",
  components: {
    CodeEditor,
    Codemirror
  },
  data(){
    return {
      selectedTab: null,
      expandDepth: 5,
      stringOutput: "test123",
      dismissSecs: 5,
      dismissCountDown: 0,
      lang: json(),
    }
  },
  methods: {
    // eslint-disable-next-line no-unused-vars
    clipboardSuccessHandler () {
      console.log('success')
      this.dismissCountDown = this.dismissSecs
      setTimeout(() => {
        this.dismissCountDown = 0
      }, 3000)
    },

    // eslint-disable-next-line no-unused-vars
    clipboardErrorHandler () {
      console.log('error')
    }
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