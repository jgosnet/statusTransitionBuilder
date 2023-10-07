<template lang="pug">
v-card(style="text-align: left").mt-2
  v-card-title Status_transition code
  v-card-text
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
      CodeMirror.py-3.w-100(v-model="jsonForm"
            :lang="lang"
          :linter="linter"
          basic
      )
</template>

<script>
import CodeMirror from 'vue-codemirror6';
import {mapGetters} from "vuex";
import {python} from "@codemirror/lang-python";
import {Clipboard} from "v-clipboard";

export default {
  name: "FormViewer",
  components:{
    CodeMirror
  },
  data(){
    return {
      lang: python(),
      linter: null,
      dismissSecs: 5,
      dismissCountDown: 0,
    }
  },
  computed:{
    ...mapGetters("status", ["jsonForm"]),
  },
  methods: {
    doCopy(){
      Clipboard.copy(this.$store.getters['status/jsonForm']);
    },
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
  }
}
</script>

<style scoped>
.cm-editor{
  min-height: 500px !important;
  max-height: 720px !important;
}
</style>