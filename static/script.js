$(document).ready(function () {
  handleGetProjects();
});

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

const handleGetProjects = () => {
  $.ajax({
    type: 'GET',
    url: '/luji_portfolio/api/v1/get_projects',
    data: {},
    success: function (res) {
      res.data.map((project) => {
        let cardHtml = `<div class="col">
            <div class="card h-100 bg-dark text-light shadow">
              <img src="../${project.project_thumbnail}" class="card-img-top" alt="Project Image" />
              <div class="card-body">
                <h5 class="card-title">
                  <a href="${project.project_link}" target="_blank" id="title">${project.project_name}<img src="../static/assets/go-to-arrow.svg" width="10px" class="pb-1 ms-1 mb-2" /></a>
                </h5>
                <p class="card-text">${project.project_desc}</p>
              </div>
            </div>
          </div>`;
        $('#card-container').append(cardHtml);
      });
    },
  });
};
