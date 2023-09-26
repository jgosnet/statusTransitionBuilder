<script>
import { ref, defineComponent } from 'vue';

import CodeMirror from 'vue-codemirror6';
import { json, jsonParseLinter } from '@codemirror/lang-json';
import {mapGetters} from "vuex";

export default defineComponent({
  components: {
    CodeMirror,
  },
  computed: {
    ...mapGetters("woPreset", ["woProviderData"]),
  },
  setup() {
    let testDict = {
      test: "123",
      test2: 123,
      test3: {
        value1: false,
      }
    }


    const value = ref(JSON.stringify(testDict, null, 2));
    const lang = json();
    const linter = jsonParseLinter();

    return { value, lang, linter};
  },
});
</script>

<template lang="pug">
div.pb-10
  CodeMirror.py-3.w-100(v-model="woProviderData"
          :lang="lang"
        :linter="linter"
        basic
    )
</template>


<style scoped>

.cm-editor{
  min-height: 500px !important;
  max-height: 720px !important;
}
</style>