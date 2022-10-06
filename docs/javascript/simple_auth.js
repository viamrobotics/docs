function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function setCookie(name, value) {
  const d = new Date();
  d.setTime(d.getTime() + (7*24*60*60*1000));
  let expires = `expires=${d.toUTCString()}`;
  document.cookie = `${name}=${value};${expires};path=/`;
}

var password;
var pass1="robotsarecool123";

if (getCookie("viam-docs-access") !== "true") {
    // never logged in, prompted for pass.
    password=prompt('Enter password or be banished to our marketing page','');
    if (password==pass1) {
        // close prompt, allow access.
        setCookie("viam-docs-access", "true");
    }
    else {
        window.location="http://viam.com/";
    }
}
