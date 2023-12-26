var loadJS = function(url, implementationCode, location) {
    var scriptTag = document.createElement('script');
    scriptTag.src = url;

    scriptTag.onload = implementationCode;
    scriptTag.onreadystatechange = implementationCode;

    location.appendChild(scriptTag);
};
var startSentry = function() {
    Sentry.onLoad(function() {
        Sentry.init({
            integrations: [
                new Sentry.Replay({
                    block: ['.table'],
                    maskAllText: false,
                    blockAllMedia: false,
                }),
            ],
        });
    });
}
loadJS('https://js.sentry-cdn.com/20c1bd502aff402ebc4c8f5c2d23878d.min.js', startSentry, document.body);
