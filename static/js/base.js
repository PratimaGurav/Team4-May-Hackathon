const googleBtn = document.querySelector('.google');

// console.log(googleBtn);

if (googleBtn) {

  // create element inside googleBtn
  googleBtn.innerHTML = '';
  const googleBtnInner = document.createElement('div');
  googleBtn.appendChild(googleBtnInner);
  googleBtnInner.classList.add('socialaccount_providers--image');
  const googleBtnInnerText = document.createElement('span');
  googleBtn.appendChild(googleBtnInnerText);
  // show a parent
  const googleBtnMainParent = googleBtn.parentElement.parentElement.parentElement.parentElement;
  console.log(googleBtnMainParent);
  // get H1 inner text of googleBtnMainParent
  const googleBtnMainParentH1 = googleBtnMainParent.querySelector('h1');
  if (googleBtnMainParentH1.innerHTML === 'Log In') {
    googleBtnInnerText.innerHTML = 'Log In with Google';
  } else {
    googleBtnInnerText.innerHTML = 'Sign Up with Google';
  }
}