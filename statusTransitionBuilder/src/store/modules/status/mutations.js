export default {
  addStep(state, payload){
    let status = payload.status || [];
    let transitions = payload.transitions || [];
    state.status.push({
      index: state.stepIndex,
      name: payload.name || `new${state.stepIndex}`,
      status: status,
      transitions: transitions,
      isExpanded: true,
    });
    state.stepIndex += 1;
  },
  updateStep(state, payload){
    console.log(payload)
    let foundItem = state.status.find(obj => obj.index === payload.index)
    console.log('found item:')
    console.log(foundItem)
    foundItem['name'] = payload.name

  },
  deleteStep(state, item){
    console.log(`trying to delete: ${item.index}`)
    console.log(item)
    state.status = state.status.filter(obj => obj.index !== item.index)
  },
  updateStepForm(state, value){
    state.stepNameForm = value;
  }
}