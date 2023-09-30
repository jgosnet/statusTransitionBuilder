<template lang="pug">
v-window-item(value="providerData" )
  v-row.my-1.ml-1
    v-btn.mx-2.my-1(
      prepend-icon="fa-solid fa-copy"

    @click="doCopy"
      v-clipboard:success="clipboardSuccessHandler"
      v-clipboard:error="clipboardErrorHandler"
      ) Copy
    v-alert.float-right(title="Copied to clipboard."
      type="success"
      color="success"
      density="compact"
      v-show="dismissCountDown > 0")

  v-row.mx-1
    CodeMirror.py-3.w-100(v-model="launcherProviderData"
          :lang="lang"
        :linter="linter"
        basic
    )

</template>

<script>
import CodeMirror from 'vue-codemirror6';
import {mapGetters} from "vuex";
import {python} from "@codemirror/lang-python";
import { Clipboard } from "v-clipboard"

export default {
  name: "LauncherPresetProviderData",
  components:{
    CodeMirror
  },
  data(){
    return {
      lang: python(),
      // linter: pythonLanguage(),
      linter: null,
      dismissSecs: 5,
      dismissCountDown: 0,
    }
  },
  computed:{
    ...mapGetters("launcherPreset", ["launcherProviderData"]),
  },
  methods: {
    doCopy(){
      Clipboard.copy(this.$store.getters['launcherPreset/launcherProviderData']);
    },
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

}
</script>

<style scoped>
.cm-editor{
  /*background-color: white !important;*/
}


</style>