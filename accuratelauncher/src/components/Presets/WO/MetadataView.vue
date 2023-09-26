<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Metadata View
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    v-row
      v-col(cols="12")
        | test

</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "MetadataView",
  data(){
    return {
      isExpanded: true,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['metadataFields']),
    expansionIcon() {
      if (this.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    },
  },
  methods: {
    addItem(){
      this.$store.dispatch("woPreset/addMetadataField")
    }
  }
}
</script>

<style scoped>

</style>