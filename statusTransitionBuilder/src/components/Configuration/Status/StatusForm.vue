<template lang="pug">
div
  v-dialog(v-model="isActive").w-50
    template(v-slot:activator="{ props }")
      v-btn(v-show="!this.statusData"
        size="small" v-bind="props")
        v-icon fa-solid fa-plus

      v-icon(color="blue" v-show="this.statusData"
        size="small"  v-bind="props") fa-solid fa-pen-to-square
    template(v-slot:default="{ isActive }")
      v-card
        v-card-title Status
        v-card-text
          v-row.px-3.py-1
            v-col(cols="3")
              v-text-field(v-model="name" hide-details
                    label="Name" density="compact" variant="outlined" )

            v-col(cols="4")
              v-combobox(v-model="group" hide-details
                    label="Group" density="compact" :items="possibleGroups" )
            v-col(cols="5")
              v-combobox(v-model="message" hide-details
                    label="Message" density="compact" :items="possibleMessages")
          //
          //v-row.px-3.py-1
          //  v-col(cols="5")
          //    v-text-field(v-model="icon" hide-details
          //          label="Icon" density="compact")
          //  v-col(cols="1").pt-5.mr-2
          //    color-picker.ml-5(v-model:pureColor="color" format="hex6")
          //  v-col(cols="3")
          //    v-text-field(v-model="color" hide-details
          //          label="Color" density="compact")
          //
          //v-row.px-3.py-1
          //  v-col(:cols="includeNotification ? 1 : 12").py-1
          //    v-checkbox(v-model="includeNotification" hide-details
          //      :label="includeNotification ? '': 'Include notification ?'" density="compact" )
          //  v-col(v-show="includeNotification" cols="6").py-1
          //    v-text-field(v-model="subject" hide-details
          //      label="Notification Subject" density="compact")
          //  v-col(v-show="includeNotification" cols="5").py-1
          //    v-combobox(v-model="endpoints" hide-details clearable=""
          //          label="Endpoints" density="compact" :items="possibleEndpoints" multiple="" chips)
          //
          //div(v-show="includeNotification")
          //  v-row.px-3.py-1()
          //    //StepItemStatusMetadata(:item="metadata")
          //
          //  v-row.px-3.py-1()
          //    v-col(cols="12").pb-2.pt-0
          //      v-combobox(v-model="attachments" hide-details clearable
          //            label="Attachments (labels)" density="compact" multiple chips)
          //

        v-card-actions
          v-spacer
          v-btn(@click="this.isActive = false") Cancel
          v-btn(@click="confirm()" :disabled="!newFormIsValid" ) confirm
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "StatusForm",
  props: ['stepIndex', 'statusData'],
  data(){
    return {
      isActive: false,
      name: '',
      group: '',
      message: '',
      icon: '',
      color: '',
      includeNotification: false,
      subject: '',
      endpoints: [],
      metadata: [],
      attachments: [],
    }
  },
  computed: {
    ...mapGetters('status', ['possibleGroups', 'possibleMessages', 'possibleEndpoints']),
    newFormIsValid(){
      return true;
    },
  },
  methods: {
    confirm(){
      this.isActive = false;

      let payload = {
        name: this.stepName
      };
      console.log(this.item);
      if (this.item && this.item.index !== undefined){
        console.log('Updating existing status');
        payload['index'] = this.item.index;
        // this.$store.dispatch('status/updateStep', payload);
      } else {
        console.log('Adding new status');
        // this.$store.dispatch('status/addStep', payload);
        this.resetForm();
      }

    },
    resetForm(){
    }
  },
  mounted() {

  }
}
</script>

<style scoped>

</style>