<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Manual markers
    //v-tooltip(text="123" )
    //  template(v-slot:activator="{ props }")
    //    v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1

  div(v-show="isExpanded" )
    v-row
      v-col(cols="12")
        ManualMarkerItem(v-for='item in manualMarkers'
            :key='item.index'
            :item="item" )

    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addItem" elevation="2" variant="outlined" ) Add New Manual Marker

        v-btn.float-right(prepend-icon="fa-solid fa-arrows-rotate"
        @click="resetManualMarkers" elevation="4" variant="outlined" ) Reset
</template>

<script>
import {mapGetters} from "vuex";
import ManualMarkerItem from "@/components/Presets/WO/Markers/ManualMarkerItem";

export default {
  name: "ManualMarkerView",
  components: {ManualMarkerItem},
  data(){
    return {
      tab: "asset",
      isExpanded: false,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['manualMarkers']),
    expansionIcon() {
      if (this.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    },
  },
  methods: {
    resetManualMarkers(){
      this.$store.dispatch("woPreset/resetManualMarkers")
    },
    addItem(){
      this.$store.dispatch("woPreset/addManualMarker")
    }
  }
}
</script>

<style scoped>
legend{
  font-size: large;
}
.noborder{
  border-style: none;
}
</style>