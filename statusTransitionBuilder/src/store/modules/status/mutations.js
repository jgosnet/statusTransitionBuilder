export default {
  addStep(state){
    state.status.push({
      index: state.stepIndex,
      name: 'new' + state.stepIndex,
      isExpanded: true,
      status: [],
      transitions: []
    });
    state.stepIndex += 1;
  },
  deleteStep(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    state.status = state.status.filter(obj => obj.index !== item.index)
  }
}