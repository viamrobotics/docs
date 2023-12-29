var snippets = document.getElementsByTagName('pre');
var code_snippets = [];

for (i = 0; i < snippets.length; i++) {
    code_snippets[i] = snippets[i].innerText;
    snippets[i].classList.add('hljs'); // append copy button to pre tag
    snippets[i].innerHTML = '<button class="hljs-copy" id="' + i + '">Copy</button>' + snippets[i].innerHTML; // append copy button
    snippets[i].getElementsByClassName('hljs-copy')[0].addEventListener("click", function () {
        this.innerText = 'Copying';
        navigator.clipboard.writeText(code_snippets[this.id]);
        this.innerText = 'Copied!';
        button = this;
        setTimeout(function () {
            button.innerText = 'Copy';
        }, 1000)
    });
}
