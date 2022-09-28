function insert(text) {
    input = document.getElementById('expression');
    old_value = input.value;
    input.value = old_value + text;
}

function clean() {
    document.getElementById('expression').value = '';
}