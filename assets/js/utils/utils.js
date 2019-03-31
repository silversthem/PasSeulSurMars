// Merges b into a recursively
function merge_dicts(a,b) {
  Object.keys(b).forEach((k) => {
    if(k in a && typeof a[k] === "object" && typeof b[k] === "object") {
      a[k] = merge_dicts(a[k],b[k])
    } else {
      a[k] = b[k]
    }
  })
  return a
}

// Creates a dict from the field/values of a html form element
function readForm(formid) {
  let form = document.getElementById(formid)
  let r = {}
  let inputs = form.getElementsByTagName('input')
  for(let i = 0;i < inputs.length;i++) {
    let input = inputs[i]
    if(['text','password'].includes(input.type)) {
      r[input.name] = input.value
    }
  }
  return r
}
