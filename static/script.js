const send_message = () => {
  let email = $('#email').val();
  let message = $('#message').val();
  console.log(email + ' ' + message);
  $.ajax({
    type: 'POST',
    url: '/contact',
    data: { email, message },
    success: function (res) {
      Swal.fire({
        title: 'Thank You!🫡',
        text: 'I will reply your message by email',
        icon: 'success',
      });
      $('#email').val('');
      $('#message').val('');
    },
  });
};
