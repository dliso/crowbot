// This file is loaded and executed when the main Crowbot page is opened.

console.log('Hello, World');

// jQuery example:

var root = 'https://jsonplaceholder.typicode.com';

$.ajax({
    url: root + '/posts/1',
    method: 'GET'
}).then(function(data) {
    console.log(data);
});
