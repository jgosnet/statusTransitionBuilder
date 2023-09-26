<template lang="pug">
fieldset.pa-1
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Spritemap details
    v-tooltip(text="123" )
      template(v-slot:activator="{ props }")
        v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1
  div(v-show="isExpanded" )
    span(v-show="Object.keys(items).length === 0" ) No Spritemap specified
    v-row.mb-0.pb-0
      v-col(cols="12").mb-0.pb-0
        v-checkbox(v-model="useSpritemap" hide-details
          label="Use Spritemap ?"
          density="compact" )
    v-row(v-show="useSpritemap" )
      v-col(cols="12")
        SpritemapDetailsItem(v-for='item in items'
            :key='items.name'
            :item="item" )
</template>

<script>
import SpritemapDetailsItem from "@/components/DPD/SpritemapSection/SpritemapDetailsItem";

export default {
  name: "SpritemapDetails",
  components: {SpritemapDetailsItem},
  computed: {
    expansionIcon(){
      if (this.isExpanded === false){
        return "fa-solid fa-caret-down"
      } else{
        return "fa-solid fa-caret-right"
      }
    },
    items: {
      get() {
        return this.$store.getters["spritemapDetails/spritemapItems"]
      }
    },
    useSpritemap: {
      get() {
        return this.$store.getters["spritemapDetails/useSpritemap"]
      },
      set(value) {
        this.$store.dispatch('spritemapDetails/updateUseSpritemap', value)
      }
    },
  },
  methods: {
  },
  data: function(){
    return {
      isExpanded: true,
    }
  },
  mounted() {
  }
}
</script>

<style scoped>

</style>