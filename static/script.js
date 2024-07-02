const send_message = () => {
  let person_sender = $('#person_sender').val();
  let message = $('#message').val();
  $.ajax({
    type: 'POST',
    url: '/contact',
    data: { person_sender, message },
    success: function (res) {
      Swal.fire({
        title: 'Thank You!🫡',
        text: 'I will reply your message by email',
        icon: 'success',
      });
      $('#person_sender').val('');
      $('#message').val('');
    },
  });
};
