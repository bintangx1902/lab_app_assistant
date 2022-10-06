const register = document.getElementById('register');
const password = document.getElementById('regpassword');
const confPassword = document.getElementById('regconfpassword');
const error = document.getElementById('error');

register.addEventListener('click', function() {
  if (password.value !== confPassword.value) {
    // setTimeout(function() {
    //   error.innerHTML = '';
    // }, 1000);
    error.innerHTML = `<div class="alert alert-danger" role="alert">
     Password do not match!
   </div>`;
  }
});

//     error.innerHTML = `<div class="alert alert-danger" role="alert">
//     Password do not match!
//   </div>`;
//   }
// });
