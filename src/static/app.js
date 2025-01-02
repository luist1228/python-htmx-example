

function toggleHidden(id){
  const el = document.getElementById(id)
  if(el.className.includes('hidden')){
    el.className = el.className
      .replace('hidden', '')
      .trim()
    
    return
  }
  el.className+=' hidden'
}


const converter = new showdown.Converter({tables: true, strikethrough: true, tasklists:true})




function togglePreview() {
  const textarea = document.getElementById("description")
  const preview = document.getElementById("preview")

  toggleHidden('description')
  // Get textarea value
  const markdown= textarea.value
  // Convert MD to html
  let htmlResult = converter.makeHtml(markdown)

  htmlResult= `${htmlResult}`
  // Set innerHtml
  preview.innerHTML=htmlResult
  toggleHidden('preview')
    
}
