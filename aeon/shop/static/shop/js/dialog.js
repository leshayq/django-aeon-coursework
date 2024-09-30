;(function () {
          
    htmx.on("htmx:afterSwap", (e) => {
      if (e.detail.target.id == "dialog") {
        $('#modal').modal('show');
      }
    })
  
    htmx.on("htmx:beforeSwap", (e) => {
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        $('#modal').modal('hide');
        e.detail.shouldSwap = false
      }
    })
  
    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = ""
    })
  })()