// JSONファイルのパス
const jsonFilePath = 'articles/articles.json';

// JSONファイルを読み込んでリンクを表示する関数
async function displayLinksFromJSON() {
    try {
        // JSONファイルを読み込む
        const response = await fetch(jsonFilePath);
        const jsonData = await response.json();

        // 更新日（lastUpdated）で降順にソート
        jsonData.links.sort((a, b) => new Date(b.lastUpdated) - new Date(a.lastUpdated));

        // リンクをリストとして表示（上位5つ）
        const linkList = document.getElementById('linkList');
        jsonData.links.slice(0, 5).forEach(link => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="${link.url}" target="_blank">${link.title}</a> (更新日: ${link.lastUpdated})`;
            linkList.appendChild(listItem);
        });
    } catch (error) {
        console.error('Error loading JSON file:', error);
    }
}

// ページ読み込み時にリンクを表示
document.addEventListener('DOMContentLoaded', displayLinksFromJSON);