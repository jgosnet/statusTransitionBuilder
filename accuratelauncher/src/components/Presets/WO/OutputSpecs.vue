<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span OutputSpecs
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

    v-row
      v-col(cols="12")


</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "OutputSpecs",
  components: {},
  data(){
    return {
      isExpanded: false,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['outputStatuses']),
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
      this.$store.dispatch("woPreset/addOutputStatus")
    }
  }
}
</script>

<style scoped>
fieldset{
  border-style: dashed;
}
</style>