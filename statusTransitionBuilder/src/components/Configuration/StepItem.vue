<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    b {{ item.name }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div(id="expand")
    v-icon.bg-transparent(:icon="expansionIcon" size="x-large"
      @click="item.isExpanded = !item.isExpanded")
  div(v-show="!item.isExpanded").py-1


  div(v-show="item.isExpanded").mb-3
    v-row.px-3.py-1
      v-col(cols="12").py-1
        v-text-field(v-model="item.name" hide-details
          label="Step name"
          density="compact" )
    v-row.px-3.py-1
      v-col(cols="12").py-1
        StepItemStatus(:item="item")

    v-row.px-3.py-1
      v-col(cols="12").py-1
        StepItemTransitions(:item="item")

</template>

<script>
import StepItemStatus from "@/components/Configuration/StepItemStatus";
import StepItemTransitions from "@/components/Configuration/StepItemTransitions";
export default {
  name: "StepItem",
  components: {StepItemTransitions, StepItemStatus},
  props: ['item'],
  computed: {
    expansionIcon() {
      if (this.item.isExpanded === false) {
        return "fa-solid fa-caret-down"
      } else {
        return "fa-solid fa-caret-right"
      }
    },
  },
  methods: {
    deleteItem(){
      this.$store.dispatch('status/deleteStep', this.item);
    }
  }
}
</script>

<style scoped>
  fieldset{
    background-color: ghostwhite;
  }
</style>