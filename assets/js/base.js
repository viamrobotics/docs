function handleAnchorClick(event, anchor) {
   // write the full anchor URL to the clipboard
   navigator.clipboard.writeText(location.href.split('#')[0] + '#' + anchor ); 

   const anchorLink = document.getElementById('anchor-link-' + anchor);
   const copiedReaction = document.getElementById('copied-' + anchor);
   const copiedReactionText = document.getElementById('copied-' + anchor + '-text');
   anchorLink.classList.add('force-visible');
   copiedReaction.classList.add('visible');
   copiedReaction.style.display = 'inline-block';
   copiedReactionText.textContent = 'Copied!';
   
   setTimeout(() => {
     anchorLink.classList.remove('force-visible');
     copiedReaction.classList.remove('visible');
     copiedReaction.style.display = 'none';
     copiedReactionText.textContent = '';
   }, 2000);
}