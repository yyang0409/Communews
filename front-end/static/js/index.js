function getRating() {
  var rate = document.querySelectorAll(".rating");
  for (var i = 0; i < rate.length; i++) {
    let stars = document.getElementsByName(rate[i].dataset.id);
    let ratingResult = document.getElementById(rate[i].dataset.id);
    let news_id = rate[i].dataset.id; // 取得新聞ID
    let newsTopic = rate[i].dataset.topic; // 取得新聞主題
    let score = parseInt(rate[i].dataset.score); // 將score轉換為整數
    let path = rate[i].dataset.path;
    console.log("路徑:",path);
    console.log("新聞ID：", news_id);
    console.log(ratingResult);
    printRatingResult(ratingResult);

    stars.forEach((star, index1) => {
      let current_star_level = index1 + 1;
      if (current_star_level <= score) {
        star.innerHTML = '&#9733'; // 填滿星星
      } else {
        star.innerHTML = '&#9734'; // 空心星星
      }

      star.onclick = function () {
        let new_rating = index1 + 1;
        console.log("新評分：", new_rating);
        // 檢查是否點擊當前星星，如果是則將評分設為0並回傳給app.py
        if (new_rating === score) {
          new_rating = 0; // 設置評分為0，即取消評分
        }

        // 更新星星填滿狀態
        stars.forEach((star, index2) => {
          if (index2 < new_rating) {
            star.innerHTML = '&#9733';
          } else {
            star.innerHTML = '&#9734';
          }
        });
        // 更新score變數的值為新評分
        score = new_rating;
        printRatingResult(ratingResult, new_rating);
        sendRatingToBackend(path,news_id, newsTopic, new_rating); // 傳遞關鍵字ID、新聞主題和評分數據
      };
    });
  }
}
//現在可以取消 但是取消歷史紀錄 沒辦法不刷新就取消


function sendRatingToBackend(path,news_id, newsTopic, rating) {
  // 使用Fetch API发送评分数据和新聞主題到后端
  fetch(path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ action: 'rating', news_id: news_id, topic: newsTopic, rating: rating }) // 將關鍵字ID、新聞主題和評分數據轉換為JSON數據傳遞
  })
    .then(response => response.json())
    .then(data => {
      // 这里可以处理后端返回的响应数据（如果有的话）
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function printRatingResult(result,num=0){
    result.textContent = `${num}/5`;
}

function listenforLike() {
    var likes = document.querySelectorAll(".like");
    
  
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
        // 從 'data-path' 屬性中獲取 'path' 的值
        var path = event.target.dataset.path;
        // 將data-id的值透過AJAX POST請求提交到Flask的app.py後端
        var xhr = new XMLHttpRequest();
        xhr.open("POST", path, true);
        xhr.setRequestHeader("Content-Type", "application/json"); 
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
        xhr.send(JSON.stringify({
          data_id: dataIdValue,
          like_status: likeStatus,
          action: 'like'
        }));
  
      });
    });
}
  


listenforLike();
getRating();
