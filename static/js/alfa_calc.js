function clean() {
    document.getElementById('expression').value = '';
}

function copy() {
    let binnary = document.getElementById('binnary').innerText;
    navigator.clipboard.writeText(binnary);
}