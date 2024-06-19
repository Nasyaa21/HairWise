$(document).ready(function () {
  // -[Animasi Scroll]---------------------------

  $(".nav-link").on("click", function () {
    $(".nav-link").removeClass("active");
    $(this).addClass("active");
  });

  $(window).scroll(function () {
    $(".slideanim").each(function () {
      var pos = $(this).offset().top;
      var winTop = $(window).scrollTop();
      if (pos < winTop + 600) {
        $(this).addClass("slide");
      }
    });

    // ScrollSpy functionality to highlight nav-link on scroll
    const sections = $("section");
    const navLinks = $(".nav-link");

    let currentSection = "";
    sections.each(function () {
      const sectionTop = $(this).offset().top;
      if ($(window).scrollTop() >= sectionTop - 60) {
        currentSection = $(this).attr("id");
      }
    });

    navLinks.each(function () {
      $(this).removeClass("active");
      if ($(this).attr("href") === `#${currentSection}`) {
        $(this).addClass("active");
      }
    });
  });

  // -[Prediksi Model]---------------------------

  // Fungsi untuk memanggil API ketika tombol prediksi ditekan
  $("#prediksi_submit").click(function (e) {
    e.preventDefault();

    $("#result-placeholder").remove();

    // Get File Gambar yg telah diupload pengguna
    var file_data = $("#input_gambar").prop("files")[0];
    var pics_data = new FormData();
    pics_data.append("file", file_data);

    $("#hasil_prediksi").html("<p>Loading...</p>");

    // Panggil API dengan timeout 1 detik (1000 ms)
    setTimeout(function () {
      try {
        $.ajax({
          url: "/api/deteksi",
          type: "POST",
          data: pics_data,
          processData: false,
          contentType: false,
          success: function (res) {
            // Ambil hasil prediksi dan path gambar yang diprediksi dari API
            res_data_prediksi = res["prediksi"];
            res_gambar_prediksi = res["gambar_prediksi"];
            var res_rekomendasi_pria = res["rekomendasi_pria"];
            var res_rekomendasi_wanita = res["rekomendasi_wanita"];

            $("#loading_indicator").hide();

            // Tampilkan hasil prediksi ke halaman web
            generate_prediksi(
              res_data_prediksi,
              res_gambar_prediksi,
              res_rekomendasi_pria,
              res_rekomendasi_wanita
            );
          },
        });
      } catch (e) {
        // Jika gagal memanggil API, tampilkan error di console
        console.log("Gagal !");
        console.log(e);
      }
    }, 1000);
  });

  // Fungsi untuk menampilkan hasil prediksi model
  function generate_prediksi(
    data_prediksi,
    image_prediksi,
    rekomendasi_pria,
    rekomendasi_wanita
  ) {
    var str = "";

    if (image_prediksi == "(none)") {
      str += "<br>";
      str += "<h4>Silahkan masukkan file gambar (.jpg)</h4>";
    } else {
      str += "<br>";
      str += "<img src='" + image_prediksi + '\' width="200"></img>';
      str += "<h3>" + data_prediksi + "</h3>";
      str += "<h5>Rekomendasi untuk Pria: " + rekomendasi_pria + "</h5>";
      str += "<h5>Rekomendasi untuk Wanita: " + rekomendasi_wanita + "</h5>";
    }
    $("#hasil_prediksi").html(str);
  }
});
