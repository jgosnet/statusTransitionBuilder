<template lang="pug">
fieldset.pa-1
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Caption details
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    span(v-show="Object.keys(captionItems).length === 0" ) No caption tracks specified
    v-row
      v-col(cols="12")
        CaptionDetailsItem(v-for='item in captionItems'
            :key='captionItems.name'
            :caption-item="item" )
    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addCaptionItem" elevation="2" variant="outlined" ) Add caption track
</template>

<script>
import CaptionDetailsItem from "@/components/DPD/CaptionSection/CaptionDetailsItem";
export default {
  name: "CaptionDetails",
  components: {CaptionDetailsItem},
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    captionItems: {
      get() {
        return this.$store.getters["captionDetails/captionItems"]
      },
      set(value) {
        this.$store.dispatch('captionDetails/updateCaptionItems', value)
      }
    },
  },
  methods: {
    addCaptionItem(){
      this.$store.dispatch("captionDetails/addNewCaptionItem")
    },
  },
  data: function(){
    return {
      isExpanded: true,
    }
  }
}
</script>

<style scoped>

</style>