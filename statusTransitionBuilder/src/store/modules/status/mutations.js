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
  },
  importConfig(state, value){
    let itemIndex = 0;
    let statusIndex = 0;
    let transitionIndex = 0;
    let operationIndex = 0;
    console.log(state);
    console.log("importing")
    console.log(value.replace(/(\w+\s* =\s*)/, '')
      .replaceAll(/\(("[\w .]+"), ("[\w .]+")\)/g, '{"name": $1, "jmespath": $2}'));
    // state.stepNameForm = value;
    const obj = JSON.parse(value.replace(/(\w+\s* =\s*)/, '')
      .replaceAll(/\(("[\w .]+"), ("[\w .]+")\)/g, '{"name": $1, "jmespath": $2}'));
    state.status = []
    for (const stepName in obj){
      let newStep = { 'index': itemIndex, 'name': stepName, 'status': [], 'transitions': [], 'isExpanded': false};
      itemIndex += 1;
      const stepItem = obj[stepName];
      console.log(stepItem);
      for (const statusName in stepItem.statuses){
        console.log(statusName)
        const statusItem = stepItem.statuses[statusName];
        console.log(statusItem)

        let newStatus = {
          "index": statusIndex,
          "name": statusName,
          "message": statusItem.message,
          "group": statusItem.group,
          "icon": statusItem.icon,
          "color": statusItem.color,
          "includeNotification": false,
          "subject": statusItem.subject || '',
          "endpoints": statusItem.endpoints || [],
          "includeMetadata": statusItem.include_metadata || [],
          "attachments": statusItem.attachments || [],
          "isExpanded": false
        }
        statusIndex += 1;

        newStep['status'].push(newStatus)
      }

      for (const transitionName in stepItem.transitions){
        console.log(transitionName)
        const transitionsList = stepItem.transitions[transitionName];
        console.log(transitionsList)

        let newTransition = {
          "index": transitionIndex,
          "name": transitionName,
          "operations": [],
          "isExpanded": false,
        }
        for (const operation of transitionsList){
          console.log('operation=');
          console.log(operation);
          let newOp = {
            "index": operationIndex,
            "opType": operation.operation,
            "type": operation.operation,
            "stepName": operation.step_name,
            "keys": operation.keys,
            "groups": operation.groups,
          }
          if (newOp.stepName){
            newOp['otherStepName'] = true;
          }

          operationIndex += 1;

          newTransition['operations'].push(newOp);
        }

        transitionIndex += 1;

        newStep['transitions'].push(newTransition)
      }

      state.status.push(newStep)
    }
  },
}