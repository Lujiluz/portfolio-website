$(document).ready(function () {
  handleGetProjects();
  // show loading overlay
  // $('.loading-overlay').fadeIn(1000);
  $(window).on('load', function () {
    $('.loading-overlay').fadeOut(1500);
  });

  // function agar gambar yang di-upload langsung ditampilkan sebagai preview
  $('#project-thumbnail').change(function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        $('#preview_img').attr('src', e.target.result).show();
      };
      reader.readAsDataURL(file);
    } else {
      $('#preview_img').hide();
    }
  });
});

// ######### SIDE BAR #########

$('#btn-toggle').click(function () {
  $('.sidebar').toggleClass('active');
});

const handleLogout = () => {
  $.ajax({
    type: 'GET',
    url: '/admin/logout',
    data: {},
    success: function (res) {
      window.location.href = res.redirect;
    },
  });
};
// ######### SIDE BAR #########

// ######### PROJECTS PAGE #########
// modal functionality
document.addEventListener('DOMContentLoaded', (event) => {
  const openModalBtn = document.getElementById('modal-new-project');
  const exampleModal = new bootstrap.Modal(document.getElementById('exampleModal'));

  openModalBtn.addEventListener('click', () => {
    exampleModal.show();
  });

  // Hide the modal after some operation
  // exampleModal.hide();
});

const handleNewProject = () => {
  const data = new FormData();
  const projectThumbnail = $('#project-thumbnail')[0].files[0];
  projectThumbnail ? data.append('project_thumbnail', projectThumbnail) : data.append('project-thumbnail', null);

  let projectName = $('#project-name').val();
  let projectLink = $('#project-link').val();
  let projectDesc = $('#project-description').val();
  data.append('project_name', projectName);
  data.append('project_link', projectLink);
  data.append('project_description', projectDesc);

  if (confirm('Apakah data sudah benar semua?')) {
    $.ajax({
      type: 'POST',
      url: '/luji_portfolio/api/v1/add_project',
      data: data,
      contentType: false,
      processData: false,
      success: function (res) {
        alert(res.msg);
        window.location.reload();
      },
    });
  }
};

const handleDeleteProject = () => {
  let project_name = $('#title').text();
  if (confirm(`are you sure you want to delete ${project_name} project, sir?`)) {
    $.ajax({
      type: 'POST',
      url: '/luji_portfolio/api/v1/delete_project',
      data: { project_name },
      success: function (res) {
        alert(res.msg);
        location.reload();
      },
    });
  }
};

const handleGetProjects = () => {
  $.ajax({
    type: 'GET',
    url: '/luji_portfolio/api/v1/get_projects',
    data: {},
    success: function (res) {
      res.data.map((project) => {
        let cardHtml = `<div class="col">
            <div class="card h-100 bg-dark text-light">
              <img src="../${project.project_thumbnail}" class="card-img-top" alt="Project Image" />
              <div class="card-body">
                <h5 class="card-title">
                  <a href="${project.project_link}" target="_blank" id="title">${project.project_name}<img src="../static/assets/github-light.svg" width="20px" class="pb-1 ms-2" /></a>
                </h5>
                <p class="card-text">${project.project_desc}</p>
                <div class="w-full d-flex justify-content-center">
                  <button type="button" class="btn btn-warning me-2"><i class="bx bx-edit"></i></button>
                  <button type="button" class="btn btn-danger ms-2" onclick="handleDeleteProject()"><i class="bx bx-trash-alt"></i></button>
                </div>
              </div>
            </div>
          </div>`;
        $('#card-container').append(cardHtml);
      });
    },
  });
};

// ######### END OF PROJECTS PAGE #########
