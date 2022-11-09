let login_field = document.getElementById('id_login')
let pass_field = document.getElementById('id_password')

$("input").removeClass('border text-gray-700 py-2 block rounded-lg w-full leading-normal appearance-none border-gray-300 bg-white focus:outline-none px-4')

login_field.className += ' intro-x login__input form-control py-3 px-4 block'
pass_field.className += ' intro-x login__input form-control py-3 px-4 block'
