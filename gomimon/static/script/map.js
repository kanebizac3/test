var map = L.map('mapid').setView([34.7032526, 135.4268819], 16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
}).addTo(map);

// 初期ロード時に地図にデータを表示する処理
fetch('/gomimon/api/map_data/')
    .then(response => response.json())
    .then(data => {
        data.forEach(item => {
            let popupContent = `報告日時: ${new Date(item.reported_at).toLocaleString()}<br>詳細: ${item.description}`;
            if (item.image_url) {
                popupContent += `<br><img src="${item.image_url}" alt="ゴミの画像" class="popup-image">`;
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