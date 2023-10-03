<template lang="pug">
fieldset.pa-1.mb-5
  legend.left-align.pl-2.font-weight-bold(@click="isExpanded = !isExpanded")
    span Custom Forms
    //v-tooltip(text="123" )
    //  template(v-slot:activator="{ props }")
    //    v-icon(v-bind="props").pl-2 fa-solid fa-circle-info
  div(id="expand")
    v-icon(:icon="expansionIcon" size="x-large"
      @click="isExpanded = !isExpanded")
  div(v-show="!isExpanded").py-1

  div(v-show="isExpanded" )
    v-row(v-for='item in forms'
            :key='item.index')
      v-col(cols="12")
        FormsViewItem(
            :item="item")

    v-row
      v-col(cols="12")
        v-btn(prepend-icon="fa-solid fa-plus"
        @click="addItem" elevation="2" variant="outlined" ) Add New Form

</template>

<script>
import {mapGetters} from "vuex";
import FormsViewItem from "@/components/Presets/WO/Forms/FormsViewItem";

export default {
  name: "FormsView",
  components: {FormsViewItem},
  data(){
    return {
      tab: "asset",
      isExpanded: false,
    }
  },
  computed: {
    ...mapGetters('woPreset', ['forms']),
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
      this.$store.dispatch("woPreset/addForm")
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