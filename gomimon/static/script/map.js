var defaultLat = 34.7032526;
var defaultLng = 135.4268819;
var defaultZoom = 16;

function changeMarkerIcon(marker, newImageUrl) {
    // 新しいアイコンを作成
    var newIcon = L.icon({
      iconUrl: newImageUrl,
      iconSize: [25, 41], // 画像のサイズに合わせて調整
      iconAnchor: [12, 41], // アイコンのどの点がマーカーの位置に対応するか
      popupAnchor: [1, -34] // ポップアップを開く位置
    });
  
    // マーカーのアイコンを新しいアイコンに設定
    marker.setIcon(newIcon);
  }
  
  // 例：既存のマーカーの変数名が `blueMarker` だとする
  // 新しい画像のURLを `new_marker_icon.png` とする
  var blueMarker; // あなたの青い印のマーカーの変数

var map = L.map('mapid').setView([defaultLat, defaultLng], defaultZoom);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

function onLocationFound(e) {
    var radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map)
        .bindPopup("あなたの現在地 (精度: " + radius + " メートル)").openPopup();
    L.circle(e.latlng, radius).addTo(map);
    map.setView(e.latlng, 16); // ユーザーの位置情報が見つかったら中心を移動
}

function onLocationError(error) {
    console.error("位置情報の取得に失敗しました:", error.message);
    // デフォルトの座標をすでに setView しているので、ここでは何もしないか、
    // エラーメッセージを表示するなどの処理を追加できます。
}

map.locate({setView: false, maxZoom: 16}); // 初回ロード時に位置情報の取得を試みる
map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

// 初期ロード時に地図にデータを表示する処理
fetch('/gomimon/api/map_data/')
    .then(response => response.json())
    .then(data => {
        data.forEach(item => {
            let popupContent = `報告日時: ${new Date(item.reported_at).toLocaleString()}<br>種類: ${item.category}`;
            if (item.image_url) {
                popupContent += `<br><img src="${item.image_url}" alt="ゴミの画像" style="max-width: 40px; max-height: 40px; cursor:pointer;" class="clickable-popup-image">`;
            }
            L.marker([item.latitude, item.longitude])
                .addTo(map)
                .bindPopup(popupContent);
        });
    })
    .catch(error => {
        console.error('地図データの取得に失敗しました:', error);
    });

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const messageContainer = document.getElementById('message-container');
    const errorsContainer = document.getElementById('errors-container');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();

        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                const formData = new FormData(uploadForm);
                formData.append('latitude', latitude);
                formData.append('longitude', longitude);

                fetch('/gomimon/submit_map_data/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        messageContainer.textContent = data.message;
                        messageContainer.className = 'success';
                        errorsContainer.textContent = '';
                        window.location.href = data.redirect_url;
                    } else {
                        messageContainer.textContent = data.message;
                        messageContainer.className = 'error';
                        if (data.errors) {
                            let errorText = 'エラー:\n';
                            for (const field in data.errors) {
                                errorText += `${field}: ${data.errors[field].join(', ')}\n`;
                            }
                            errorsContainer.textContent = errorText;
                        } else {
                            errorsContainer.textContent = '';
                        }
                    }
                })
                .catch(error => {
                    console.error('Fetch APIエラー:', error);
                    messageContainer.textContent = '投稿に失敗しました。';
                    messageContainer.className = 'error';
                    errorsContainer.textContent = error;
                });
            }, showError); // 位置情報取得失敗時の処理
        } else {
            alert("このブラウザは位置情報に対応していません。");
        }
    });
});

function showError(error) {
    let errorMessage = "";
    switch(error.code) {
        case error.PERMISSION_DENIED:
            errorMessage = "位置情報の利用が拒否されました。";
            break;
        case error.POSITION_UNAVAILABLE:
            errorMessage = "位置情報が利用できません。";
            break;
        case error.TIMEOUT:
            errorMessage = "位置情報の取得がタイムアウトしました。";
            break;
        case error.UNKNOWN_ERROR:
            errorMessage = "不明なエラーが発生しました。";
            break;
    }
    alert(errorMessage);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = cookie.substring(name.length + 1);
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('click', function (e) {
    if (e.target.classList.contains('clickable-popup-image')) {
        const overlay = document.getElementById('image-popup-overlay');
        const popupImg = document.getElementById('popup-image');
        popupImg.src = e.target.src;
        overlay.style.display = 'flex';
    } else if (e.target.id === 'image-popup-overlay') {
        e.target.style.display = 'none';
    }
});