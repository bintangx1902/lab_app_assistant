let username_field = document.getElementById('id_username')
let email_field = document.getElementById('id_email')
let pass1 = document.getElementById('id_password1')
let pass2 = document.getElementById('id_password2')

$("input").removeClass('border text-gray-700 py-2 block rounded-lg w-full leading-normal appearance-none border-gray-300 bg-white focus:outline-none px-4')

username_field.className += ' intro-x login__input form-control py-3 px-4 block'
email_field.className += ' intro-x login__input form-control py-3 px-4 block'
pass1.className += ' intro-x login__input form-control py-3 px-4 block'
pass2.className += ' intro-x login__input form-control py-3 px-4 block'