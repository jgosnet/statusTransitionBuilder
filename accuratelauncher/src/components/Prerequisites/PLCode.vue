<template lang="pug">
v-window-item(:value="item" )
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
    CodeMirror.py-3.w-100(v-model="code"
          :lang="lang"
        :linter="linter"
        basic
    )
</template>

<script>
import CodeMirror from "vue-codemirror6";
import {Clipboard} from "v-clipboard";
import {python} from "@codemirror/lang-python";

export default {
  name: "PLCode",
  components:{
    CodeMirror
  },
  props: ['item'],
  data(){
    return {
      lang: python(),
      linter: null,
      dismissSecs: 5,
      dismissCountDown: 0,
    }
  },
  computed:{
    code(){
      if (this.item === '__pl_accurate'){
        return this.$store.getters['prerequisites/pl_accurate']
      } else if (this.item === '__pl_logging'){
        return this.$store.getters['prerequisites/pl_logging']
      } else if (this.item === '__pl_technical'){
        return this.$store.getters['prerequisites/pl_technical']
      } else if (this.item === '__pl_files'){
        return this.$store.getters['prerequisites/pl_files']
      }
      return ''
    }
  },
  methods:{
    doCopy(){
      Clipboard.copy(this.code);
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
  }
}
</script>

<style scoped>
.cm-editor{
  min-height: 500px !important;
  max-height: 720px !important;
}
</style>