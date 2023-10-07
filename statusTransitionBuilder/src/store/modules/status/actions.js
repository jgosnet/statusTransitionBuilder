export default {
  addStep(context, payload){
    context.commit('addStep', payload);
  },
  updateStep(context, payload){
    context.commit('updateStep', payload);
  },
  deleteStep(context, item){
    context.commit('deleteStep', item);
  },
  updateStepForm(context, value){
    context.commit('updateStepForm', value)
  }
}