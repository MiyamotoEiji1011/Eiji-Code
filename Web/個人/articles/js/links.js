// JSONファイルのパス
const jsonFilePath = '../../articles.json';

// JSONファイルを読み込んでリンクを表示する関数
async function displayLinksFromJSON() {
    try {
        const response = await fetch(jsonFilePath);
        const jsonData = await response.json();

        jsonData.links.sort((a, b) => new Date(b.lastUpdated) - new Date(a.lastUpdated));

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