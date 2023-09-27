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
        OutputSpecsItem(v-for='item in outputSpecs'
            :key='item.index'
            :item="item" )
    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addItem" elevation="2" variant="outlined" ) Add New OutputSpec

        v-btn.float-right(prepend-icon="fa-solid fa-arrows-rotate"
        @click="resetOutputSpecs" elevation="4" variant="outlined" ) Reset outputSpecs


</template>

<script>
import {mapGetters} from "vuex";
import OutputSpecsItem from "@/components/Presets/WO/OutputSpecsItem";

export default {
  name: "OutputSpecs",
  components: {OutputSpecsItem},
  data(){
    return {
      isExpanded: true,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['outputSpecs']),
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
      this.$store.dispatch("woPreset/addOutputSpec")
    },
        resetOutputSpecs(){
      this.$store.dispatch("woPreset/resetOutputSpecs")
    }
  },
  mounted() {
    this.$store.dispatch("woPreset/resetOutputSpecs")
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