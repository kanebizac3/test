function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("このブラウザは位置情報に対応していません。");
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // フォームの緯度・経度フィールドを取得 (name属性に基づいて)
    const latitudeInput = document.querySelector('input[name="latitude"]');
    const longitudeInput = document.querySelector('input[name="longitude"]');

    if (latitudeInput && longitudeInput) {
        latitudeInput.value = latitude;
        longitudeInput.value = longitude;
        console.log('取得した緯度:', latitude, '経度:', longitude);
    } else {
        console.error('緯度または経度の入力フィールドが見つかりません。フォームのname属性を確認してください。');
    }

    // 座標をDjangoサーバーに送信してリダイレクトする処理 (fetch APIを使用)
    fetch('/save_location/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // DjangoのCSRFトークンを取得
        },
        body: JSON.stringify({ latitude: latitude, longitude: longitude }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success' && data.redirect_url) {
            console.log('サーバーからの応答:', data);
            // window.location.href = data.redirect_url; // サーバーから提供されたURLにリダイレクト
        } else {
            console.error('サーバーからの応答エラー:', data);
        }
    })
    .catch(error => {
        console.error('Fetch APIエラー:', error);
    });
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("位置情報の利用が拒否されました。");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("位置情報が利用できません。");
            break;
        case error.TIMEOUT:
            alert("位置情報の取得がタイムアウトしました。");
            break;
        case error.UNKNOWN_ERROR:
            alert("不明なエラーが発生しました。");
            break;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // 指定されたnameで始まるクッキーを見つける
            if (cookie.startsWith(name + '=')) {
                cookieValue = cookie.substring(name.length + 1);
                break;
            }
        }
    }
    return cookieValue;
}

// ページ読み込み時ではなく、ボタンクリック時にgetLocation()を呼び出すように変更
// document.addEventListener('DOMContentLoaded', function() {
//     const getLocationButton = document.getElementById('getLocationButton');
//     if (getLocationButton) {
//         getLocationButton.addEventListener('click', getLocation);
//     }
// });