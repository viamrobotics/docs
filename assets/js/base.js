function handleAnchorClick(event, anchor) {
   // write the full anchor URL to the clipboard
   navigator.clipboard.writeText(location.href.split('#')[0] + '#' + anchor ); 

   const copiedReaction = document.getElementById('copied-' + anchor);
   const copiedReactionText = document.getElementById('copied-' + anchor + '-text');
   copiedReaction.classList.add('visible');
   copiedReactionText.textContent = 'Copied!';
   
   setTimeout(() => {
     copiedReaction.classList.remove('visible');
     copiedReactionText.textContent = '';
   }, 2000);
}