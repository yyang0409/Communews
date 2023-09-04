const record_views = () => {
    let views = document.querySelectorAll(".news_link");
    console.log(views)
    views.forEach((view) => {
        console.log(view);
            let news_id = view.dataset.id;
            let path = view.dataset.path;
            let keyword_weight = view.dataset.keyword;
            console.log(news_id);
            console.log(path);
            console.log(keyword_weight);
            view.addEventListener('click', function(event){
                console.log(event);
                sendViewToBackend(path,news_id,keyword_weight);
            });
    });

} // end of record_views
const sendViewToBackend = (path,news_id,keyword_weight) => {
    var responseClone; // 1
    fetch(path,{
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({action:'view',news_id:news_id,keyword_weight:keyword_weight})
    }).then(function(response){
        responseClone = response.clone(); // 2
        response.json();
    })
    .catch((error) => {
        console.log(`Error: ${error}`);
    })
}// end of sendViewToBackend

record_views();