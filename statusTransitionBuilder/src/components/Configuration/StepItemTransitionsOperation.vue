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
        v-card.mb-2.py-0(elevation="6" )
          v-card-text.ma-0.pa-1
            v-row.px-3.pt-1
              v-col(cols="1")
                v-icon.handle1.float-left fa-solid fa-bars
              v-col(cols="3")
                v-select(v-model="element.opType" hide-details
                              label="Type" density="compact" :items="possibleOperations")
              v-col(cols="7")
                v-select(v-model="element.keys" hide-details :items="possibleOperations" multiple
                              label="Keys" density="compact")
              v-col(cols="1")
                v-icon.handle.float-right(color="red" @click="deleteOperation(element)" size="x-large" ) fa-solid fa-xmark

            v-row.px-3.py-1
              v-col(:cols="element.otherStepName ? 1 : 12").py-1
                v-checkbox(v-model="element.otherStepName" hide-details
                  :label="element.otherStepName ? '': 'select step name ?'" density="compact" )
              //v-col(v-show="element.includeNotification" cols="6").py-1
              //  v-text-field(v-model="element.subject" hide-details
              //    label="Notification Subject" density="compact")
              //v-col(v-show="element.includeNotification" cols="5").py-1
              //  v-combobox(v-model="element.endpoints" hide-details clearable=""
              //        label="Endpoints" density="compact" :items="possibleEndpoints" multiple="" chips)
</template>

<script>
import draggable from "vuedraggable";
import {mapGetters} from "vuex";


export default {
  name: "StepItemTransitionsOperation",
  components: {
    draggable
  },
  computed: {
    ...mapGetters('status', ['possibleOperations']),
    summarizedList(){
      let res = "";
      for (const operation in this.item.operations){
        if (!res){
          res = operation.opType;
        }
        res += ", "+ operation.opType;
      }
      return res
    }
  },
  props: ['item'],
  methods: {
    addOperation(){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.operations.push({
        index: this.item.operationIndex,
        type: 'add_marker',
      });
      // eslint-disable-next-line vue/no-mutating-props
      this.item.operationIndex += 1;
    },
    deleteOperation(element){
      // eslint-disable-next-line vue/no-mutating-props
      this.item.operations = this.item.operations.filter(obj => obj.index !== element.index);
    }
  }
}
</script>

<style scoped>

</style>