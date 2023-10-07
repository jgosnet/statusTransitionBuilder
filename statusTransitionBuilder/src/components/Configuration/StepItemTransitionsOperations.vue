<template lang="pug">
v-row.px-3.pt-1
  v-col(cols="1").py-1.my-0
    v-btn(size="small" @click="addOperation()")
      v-icon fa-solid fa-plus
  v-col(cols="11").py-1.my-0.mb-3
    span(v-show="!item.operations.length" ) No Operations.

    draggable(v-model="item.operations"
            handle=".handle1"
            :group="item.index"
            @start="drag=true"
            @end="drag=false"
            item-key="index").w-100

      template(#item="{element}")
        StepItemTransitionsOperationItem(:item="element" :parent="parent")

</template>

<script>
import draggable from "vuedraggable";
import {mapGetters} from "vuex";
import StepItemTransitionsOperationItem from "@/components/Configuration/StepItemTransitionsOperationItem";


export default {
  name: "StepItemTransitionsOperations",
  components: {
    StepItemTransitionsOperationItem,
    draggable
  },
  computed: {
    ...mapGetters('status', ['possibleOperations', 'statusList']),
  },
  props: ['item', 'parent'],
  methods: {
    addOperation(){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.operations.push({
        index: this.item.operationIndex,
        type: 'add_marker',
        otherStepName: false,
        stepName: '',
      });
      // eslint-disable-next-line vue/no-mutating-props
      this.item.operationIndex += 1;
    }
  },
}
</script>

<style scoped>

</style>