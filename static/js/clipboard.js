const copyButtons = document.querySelectorAll('.copyButton');
var msgArea = document.getElementsByClassName('success-msg')[0];

copyButtons.forEach(button => {
    button.addEventListener('click', function () {
        const tagText = this.previousElementSibling;
        const message = this.nextElementSibling;

        const tagValue = tagText.value;
        copyToClipboard(tagValue, message);

    });
});

function copyToClipboard(tagValue) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(tagValue)
        // フラッシュメッセージ表示
        msgArea.classList.remove('del');
        msgArea.classList.add('show');

        // 3秒後にクラスを削除
        setTimeout(() => {
            msgArea.classList.remove('show');
            msgArea.classList.add('del');

        }, 1000);
    }
}

