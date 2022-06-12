const googleBtn = document.querySelector('.google');

console.log(googleBtn);

if (googleBtn) {

  // create element inside googleBtn
  googleBtn.innerHTML = '';
  const googleBtnInner = document.createElement('div');
  googleBtn.appendChild(googleBtnInner);
  googleBtnInner.classList.add('socialaccount_providers--image');
  const googleBtnInnerText = document.createElement('span');
  googleBtn.appendChild(googleBtnInnerText);
  googleBtnInnerText.innerHTML = 'Start with Google';
}