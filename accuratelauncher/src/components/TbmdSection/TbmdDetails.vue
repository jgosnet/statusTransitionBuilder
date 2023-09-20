<template lang="pug">
fieldset.pa-1
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span TBMD details
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    span(v-show="Object.keys(tbmdItems).length === 0" ) No TBMD specified
    v-row
      v-col(cols="12")
        TbmdDetailsItem(v-for='item in tbmdItems'
            :key='tbmdItems.name'
            :item="item" )
    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addTbmdItem" elevation="2" ) Add TBMD file
</template>

<script>
import TbmdDetailsItem from "@/components/TbmdSection/TbmdDetailsItem";

export default {
  name: "TbmdDetails",
  components: {TbmdDetailsItem},
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    tbmdItems: {
      get() {
        return this.$store.getters["tbmdDetails/tbmdItems"]
      },
      set(value) {
        this.$store.dispatch('tbmdDetails/updateTbmdItems', value)
      }
    },
  },
  methods: {
    addTbmdItem(){
      this.$store.dispatch("tbmdDetails/addNewTbmdItem")
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