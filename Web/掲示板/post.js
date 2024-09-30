const firebaseConfig = {
    apiKey: "AIzaSyBm137sVWfEgdffxWJqWDvKx3zQsqq5ZBE",
    authDomain: "sangikousen-keijiban.firebaseapp.com",
    projectId: "sangikousen-keijiban",
    storageBucket: "sangikousen-keijiban.appspot.com",
    messagingSenderId: "813201806133",
    appId: "1:813201806133:web:d6f98be506ca301a4b327c",
    measurementId: "G-1P9F4LNM1T"
};

// Firebaseの初期化
firebase.initializeApp(firebaseConfig);

// Firebase Firestoreの初期化
const db = firebase.firestore();


// 新着メッセージの表示数を設定
const maxMessagesToShow = 5;

function fetchMessages() {
    var messagesDiv = document.getElementById('messages');

    // Firestoreからデータを取得して表示
    db.collection('messages').orderBy('timestamp', 'desc').limit(maxMessagesToShow).get()
        .then(function (querySnapshot) {
            messagesDiv.innerHTML = ''; // 既存のメッセージをクリア

            querySnapshot.forEach(function (doc) {
                var messageContainer = document.createElement('div');
                messageContainer.classList.add('message-container');

                var usernameElement = document.createElement('p');
                usernameElement.classList.add('username');
                usernameElement.textContent = doc.data().username + ' - ' + formatTimestamp(doc.data().timestamp);

                var messageElement = document.createElement('p');
                messageElement.classList.add('message');
                messageElement.textContent = doc.data().message;

                messageContainer.appendChild(usernameElement);
                messageContainer.appendChild(messageElement);

                messagesDiv.appendChild(messageContainer);
            });
        })
        .catch(function (error) {
            console.error('Error getting documents: ', error);
        });
}


// タイムスタンプをフォーマットする関数
function formatTimestamp(timestamp) {
    const date = timestamp.toDate();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// 一定間隔でメッセージを更新する処理
setInterval(fetchMessages, 3000);

// 初回表示
fetchMessages();