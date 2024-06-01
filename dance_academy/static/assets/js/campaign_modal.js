
    /*
========================================
Submit the Modal form On Click 

once button is clicked it shows the spineer and button is hide, specific form id data is passes to submit the for 

========================================
*/






function setSuccessData(data, order_id) {
    var url = "/reel/order/" + order_id;
    // console.log(url);
    return `
<p class="text-center modal-list-item success-msg"> ${data} </p>
<p class="text-center modal-list-item">please complete the payment to proceed.. </p>

<div class="d-flex justify-content-around flex-wrap mt-1">

<span class="text-white" onclick="setPaymentSession('${order_id}')"> <button class="modal__btn">

Pay Now &rarr;
</button>
</span>


<a href="${url}" class="text-white">  <button class="modal__btn">
  View Order &rarr;
  </button>
</a>   

  `;
  }

  $(document).on("submit", "#campaignForm", function (e) {
    e.preventDefault();
    //Show the loading spinner
    $(".spinner-border.campaignSubmitBtn").show();

    //disable the button
    let button = e.target.querySelector("#campaignSubmitbtn");
    button.disabled = true;

    let songName = e.target.querySelector("#campaignSongName").value;
    let songLink = e.target.querySelector("#campaignReelLink").value;
    let tags = e.target.querySelector("#campaignTags").value;
    let id = e.target.getAttribute("data-id");

    $.ajax({
      type: "POST",
      url: "/reel/submitCampaign",
      data: {
        id: id,
        song_name: songName,
        song_link: songLink,
        tags: tags,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      //XMLhttprequest
      xhr: function () {
        var xhr = $.ajaxSettings.xhr();
        xhr.upload.onprogress = function (e) {};
        return xhr;
      },

      //if sucess
      success: function (json) {
        //hide spineer passing modal class from include tag from modal page
        $(".spinner-border.campaignSubmitBtn").hide();
        //enable button
        button.disabled = false;
        if (json.status == 1) {
          //Wrapping the services with p element
          $(".modal#" + id + " .modal-service-details").hide();
          $(".modal#" + id + " .modal-submit-success").show();
          document.querySelector(
            ".modal#" +
              id +
              " .modal-submit-success .thank-content .custome-success-msg"
          ).innerHTML = setSuccessData(json.success_msg, json.order_id);
        } else {
          // custom error message

          $(
            ".modal#" + id + " .modal-service-details #campaignForm"
          ).removeClass("alert");
          $(".modal#" + id + " .modal-service-details #campaignForm").prepend(
            "<div class='alert alert-danger' style='left:0;top:0;width:100%;'>" +
              json.data +
              "</div>"
          );
          $(".modal#" + id + " .modal-service-details #campaignForm .alert")
            .delay(10000)
            .fadeOut();
        }
      },

      error: function (xhr, errmsg, err) {
        //button enabled and spiner hide
        button.disabled = false;
        $(".spinner-border.campaignSubmitBtn").hide();

        $(
          ".modal#" + id + " .modal-service-details #campaignForm"
        ).removeClass(".alert");
        $(".modal#" + id + " .modal-service-details #campaignForm").prepend(
          "<div class='alert alert-danger' style='top:0;left:0;width:100%;'>" +
            err +
            "</div>"
        ); // add the error to the dom
        $(".modal#" + id + " .modal-service-details #campaignForm .alert")
          .delay(10000)
          .fadeOut();
      },
    });
  });

  //Load the services into modal popup form
  function getModalServices(data) {
    let content = "";

    for (let i = 0; i < data.length; i++) {
      content += "<p class='modal-list-item'>" + data[i] + "</p>";
    }

    return content;
  }

  function LoadModalData() {
    $(".campaignViewButton").on("click", (e) => {
      //get the data-search attribute from the button
      let button = e.target;

      let id = button.getAttribute("data-search");

      $(".spinner-border.modal").show();

      $.ajax({
        type: "GET",
        url: "/reel/modalServices",
        data: {
          id: id,
        },

        //XMLhttprequest
        xhr: function () {
          var xhr = $.ajaxSettings.xhr();
          xhr.upload.onprogress = function (e) {};
          return xhr;
        },

        //if sucess
        success: function (json) {
          //hide spineer passing modal class from include tag from modal page
          $(".spinner-border.modal").hide();

          if (json.status == 1) {
            //Wrapping the services with p element
            document.querySelector(".modalServiceRequest#" + id).innerHTML =
              getModalServices(json.data);
            //show the campaign final budget at the end of modal pop up
            document.querySelector(
              ".modal#" + id + " #campaign-gst-cost"
            ).innerHTML = `${json.display_budget}`;
          } else {
            // custom error message
            $(".modalServiceRequest#" + id).removeClass("alert");
            $(".modalServiceRequest#" + id).prepend(
              "<div class='alert alert-danger' style='left:0;top:0;width:100%;'>" +
                json.data +
                "</div>"
            );
            $(".modalServiceRequest#" + id + ".alert")
              .delay(10000)
              .fadeOut();
          }
        },

        error: function (xhr, errmsg, err) {
          $(".spinner-border.modal").hide();

          $(".modalServiceRequest#" + id).removeClass(".alert");
          $(".modalServiceRequest#" + id).prepend(
            "<div class='alert alert-danger' style='top:0;left:0;width:100%;'>" +
              err +
              "</div>"
          ); // add the error to the dom
          $(".modalServiceRequest#" + id + ".alert")
            .delay(10000)
            .fadeOut();
        },
      });
    });
  }
