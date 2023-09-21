<template lang="pug">
v-card.rounded-lg.mx-0
  v-card-title(@click="isExpanded = !isExpanded")
    span Import existing configuration
    v-icon.float-right(:icon="expansionIcon" size="large")
  v-card-text.w-100(v-show="isExpanded" ).float-left
    code-mirror.w-100.CodeMirror(v-model="importValue"
      basic :lang="lang"
      )
    v-btn.float-left import
</template>

<script>
import CodeMirror from 'vue-codemirror6';
import { json } from '@codemirror/lang-json';

export default {
  name: "TheImporter",
  components: {
    CodeMirror
  },
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
  },
  data(){
    return {
      isExpanded: false,
      importValue: "test",
      lang: json(),
    }
  },
}
</script>

<style scoped>
.CodeMirror {
  border: 1px solid #eee;
  height: 250px;
  text-align: left;
}
</style>