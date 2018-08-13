Vue.component('index_table_row', {
    template: `
        <tr>
            <td><a v-bind:href="'books/' + book.id">{{ book.isbn }}</a></td>
            <td><a v-bind:href="'books/' + book.id">{{ book.title }}</a></td>
            <td>{{ book.author }}</td>
            <td>{{ book.year }}</td>
        </tr>
    `,
    props: ['book'],
});

let app = new Vue({
    el: '#index_target',
    data: {
        books: {},
        options: {
            limit: '100',
            page: '',
            search: '',
        },
    },
    methods: {
        updateList: function () {
            fetchBooks();
        },
    },
});


function fetchBooks() {
    console.log('fired');
    fetch('/api/books', {
        body: JSON.stringify(app.options),
        headers: {
            'content-type': 'application/json'
        },
        credentials: 'include',
        method: 'POST',
    })
        .then((response) => {
            return response.json();
        })
        .then((response) => {
            app.books = response.books;
        });
}

onload = (() => {
    fetchBooks();
})();