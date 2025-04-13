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

    const latitudeInput = document.getElementById('latitudeInput');
    const longitudeInput = document.getElementById('longitudeInput');

    if (latitudeInput && longitudeInput) {
        latitudeInput.value = latitude;
        longitudeInput.value = longitude;
        console.log('取得した緯度:', latitude, '経度:', longitude);
    } else {
        console.error('緯度または経度の入力フィールドが見つかりません。フォームのname属性を確認してください。');
    }
}

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
    alert(errorMessage); // エラーメッセージをアラートで表示
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

// ページロード時に位置情報を取得するように変更
document.addEventListener('DOMContentLoaded', getLocation);