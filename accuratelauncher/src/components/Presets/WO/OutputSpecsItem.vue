<template lang="pug">
fieldset.dashed-border.pa-1
  legend.left-align.pl-2
    | {{ item.regexp }}
    v-icon.ml-3(@click="deleteItem"
      size="x-small" ) fa-solid fa-trash-can
  div()
    v-row.px-3.py-1
      v-col(cols="6").py-1
        v-text-field(v-model="item.regexp" hide-details
          label="Regexp" density="compact" prepend-icon="fa-solid fa-magnifying-glass")
      v-col(cols="6").py-1
        v-text-field(v-model="item.label" hide-details
          label="Label" density="compact" prepend-icon="fa-solid fa-file-signature")

    v-row.px-3.py-1.my-0
      v-col(cols="4").py-1.my-0
        v-text-field(v-model="item.location" hide-details
          label="RSL" density="compact" )

      v-col(cols="8").py-1.my-0
        v-text-field(v-model="item.name" hide-details
          label="Output Name (with prefix)" density="compact" )

</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "OutputSpecsItem",
  props:["item"],
  methods: {
    deleteItem(){
      console.log(`deleting asset status item:`)
      console.log(this.item)
      this.$store.dispatch("woPreset/deleteOutputSpec", this.item)
    }
  },
  computed: {
    ...mapGetters('woPreset', ['possibleStatusColors']),
    statusColor(){
      console.log(this.item.color)
      // eslint-disable-next-line no-undef
      switch(this.item.color) {
        case "var(--AP-SUCCESS)":
          return "green"
        case "var(--AP-ERROR)":
          return "red"
        case "var(--AP-FOREGROUND-2)":
          return "blue"
      }
      return ""
    },
  }
}
</script>

<style scoped>
.red{
  background-color: indianred;
}

.green{
  background-color: lightgreen;
}

.blue{
  background-color: lightskyblue;
}
fieldset{
background-color: whitesmoke;
}

</style>