function getRating(){
    var  rate = document.querySelectorAll(".rating");
    // console.log(rate);
    for(var i=0; i<rate.length; i++){
        let stars = document.getElementsByName(rate[i].dataset.id)
        // console.log(stars)
        let ratingResult = document.getElementById(rate[i].dataset.id)
        console.log(ratingResult)
        printRatingResult(ratingResult);

        stars.forEach((star,index1)=> {
            // console.log(star)
            // star.addEventListener("click",() => {
            //     stars.forEach((star,index2) => {
            //     index1 >= index2 ? star.classList.add("active") : star.classList.remove("active");
            //     console.log(index1);
            // });
            star.onclick = function() {
                // console.log(star)
                let current_star_level = index1+1;
                console.log(index1+1)
                stars.forEach((star,index2) => {

                    console.log(index2)
                    if(current_star_level >= index2+1 )
                    {
                        star.innerHTML = '&#9733';
                    } else{
                        star.innerHTML = '&#9734';
                    }
                });
                printRatingResult(ratingResult,index1+1); 
            };
               
            // 取最後一個 index1 為評分的值 需要+1 因為index從0開始計算
            
        });
    }

}


function printRatingResult(result,num=0){
    result.textContent = `${num}/5`;
}

function listenforLike() {
    var likes = document.querySelectorAll(".like");
    console.log(likes);
  
    likes.forEach(like => {
      like.addEventListener("click", (event) => {
        event.target.classList.toggle("like-no");
        event.target.classList.toggle("like-yes");
        if (event.target.classList.contains("like-yes")) {
          console.log("Saving Favorite...");
        } else {
          console.log("Remove Favorite...");
        }
        var likeStatus = event.target.classList.contains("like-yes") ? "Y" : "N";
        console.log("Like status:", likeStatus);
        // 獲取data-id的值
        var dataIdValue = like.dataset.id;
  
        // 將data-id的值透過AJAX POST請求提交到Flask的app.py後端
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/hot", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = function() {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
              // 成功回傳時執行的程式碼
              console.log("成功回傳到Flask後端！");
              console.log(xhr.responseText); // 如果Flask回傳了任何東西，會在瀏覽器的開發者工具中顯示
            } else {
              // 發生錯誤時執行的程式碼
              console.log("傳送至Flask後端時發生錯誤！");
              console.log(xhr.status);
            }
          }
        };
        xhr.send("data_id=" + encodeURIComponent(dataIdValue)+ "&like_status=" + likeStatus); // 使用表單格式提交資料
      });
    });
}
  


listenforLike();
getRating();
