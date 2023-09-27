<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Asset Status
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    span(v-show="Object.keys(outputStatuses).length === 0" ) No status specified
    v-row
      v-col(cols="12")
        AssetStatusItem(v-for='item in outputStatuses'
            :key='item.index'
            :item="item" )
    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addItem" elevation="2" variant="outlined" ) Add New Status

</template>

<script>
import {mapGetters} from "vuex";
import AssetStatusItem from "@/components/Presets/WO/AssetStatusItem";

export default {
  name: "AssetStatus",
  components: {AssetStatusItem},
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

legend{
  font-size: large;
}
</style>