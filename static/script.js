const send_message = () => {
  let person_sender = $('#person_sender').val();
  let message = $('#message').val();

  if (person_sender == '' || message == '') {
    return Swal.fire({
      title: 'Cannot send message! ❌',
      text: 'Please complete the form 🙏',
      icon: 'warning',
    });
  }
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
