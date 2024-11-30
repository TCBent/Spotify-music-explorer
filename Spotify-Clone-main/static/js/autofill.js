// fetch asincrono para hacer el autofill de generos

document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('userInput');
    const autocompleteList = document.getElementById('autocomplete-list');

    userInput.addEventListener('input', function() {
        const query = this.value;
        if (query.length > 0) {
            fetch(`/get_genres?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    autocompleteList.innerHTML = '';
                    data.forEach(item => {
                        const suggestion = document.createElement('div');
                        suggestion.classList.add('autocomplete-suggestion');
                        suggestion.textContent = item;
                        suggestion.addEventListener('click', function() {
                            userInput.value = item;
                            autocompleteList.innerHTML = '';
                        });
                        autocompleteList.appendChild(suggestion);
                    });
                });
        } else {
            autocompleteList.innerHTML = '';
        }
    });

    document.addEventListener('click', function(e) {
        if (e.target !== userInput) {
            autocompleteList.innerHTML = '';
        }
    });
});