<template lang="pug">
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
    CodeMirror.py-3.w-100(v-model="woRallyConfig"
          :lang="lang"
        :linter="linter"
        basic
    )
</template>

<script>
import CodeMirror from "vue-codemirror6";
import {mapGetters} from "vuex";
import {json, jsonParseLinter} from "@codemirror/lang-json";

export default {
  name: "RallyConfig",
  components:{
    CodeMirror
  },
  data(){
    return {
      lang: json(),
      linter: jsonParseLinter(),
      dismissSecs: 5,
      dismissCountDown: 0,
    }
  },
  computed:{
    ...mapGetters("woPreset", ["woRallyConfig"]),
  },
  methods:{
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
  }
}
</script>

<style scoped>
.cm-editor{
  min-height: 500px !important;
  max-height: 720px !important;
}
</style>