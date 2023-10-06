export default {
  addStep(context){
    context.commit('addStep');
  },
  deleteStep(context, item){
    context.commit('deleteStep', item);
  },
}