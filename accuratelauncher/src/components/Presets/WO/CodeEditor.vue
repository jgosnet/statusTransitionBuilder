<script>
import { ref, defineComponent } from 'vue';

import CodeMirror from 'vue-codemirror6';
import { json, jsonParseLinter } from '@codemirror/lang-json';
import {oneDark } from "@codemirror/theme-one-dark"

export default defineComponent({
  components: {
    CodeMirror,
  },
  computed: {

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
    const dark = true;
    const theme = oneDark;

    return { value, lang, linter, dark, theme};
  },
});
</script>

<template lang="pug">
CodeMirror.py-3.w-100(v-model="value"
      :lang="lang"
    :linter="linter"
    :dark="dark"
    basic
)
</template>


<style scoped>

</style>