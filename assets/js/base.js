function handleAnchorClick(anchor) {
   // write the full anchor URL to the clipboard
   navigator.clipboard.writeText(location.href.split('#')[0] + '#' + anchor ); 

   const checkmark = document.getElementById('checkmark-' + anchor);
   checkmark.classList.add('visible');
   
   setTimeout(() => {
     checkmark.classList.remove('visible');
   }, 2000);
}