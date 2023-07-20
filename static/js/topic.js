//   會反白現在是在哪個主題 
function focuspage(){
    var topicname = $("span.topicname").text()
    var topictabs = document.querySelectorAll(".topic-tab")

    topictabs.forEach((tab) =>{
    if(tab.textContent == topicname){
        tab.classList.add('active')
    }      
    })
}

focuspage();