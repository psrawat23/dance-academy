// review my code
function reelHistoryPagination(maxRow,table,paginator) {

  var lastPage = 1;
  $(maxRow)
    .on("change", function (evt) {
      //$('.paginationprev').html('');						// reset pagination
      lastPage = 1;
      $(paginator).find("li").slice(1, -1).remove();
      var trnum = 0; // reset tr counter
      console
      var maxRows = parseInt($(maxRow).val()); // get Max Rows from select option

      if (maxRows == 5000) {
        $(paginator).hide();
      } else {
        $(paginator).show();
      }

      // rowTrue is used to caclulate number of rows only which are searched 

      var totalRows = $(table + " tbody tr.reel_history_tr.rowTrue").length; // numbers of rows
    
      $(table + " tbody tr.reel_history_tr.rowTrue").each(function () {
        // each TR in  table and not the header
        trnum++; // Start Counter
        if (trnum > maxRows) {
          // if tr number gt maxRows

          $(this).hide(); // fade it out
        }
        if (trnum <= maxRows) {
          $(this).show();
        } // else fade in Important in case if it ..
      }); //  was fade out to fade it in
      if (totalRows > maxRows) {
        // if tr total rows gt max rows option
        var pagenum = Math.ceil(totalRows / maxRows); // ceil total(rows/maxrows) to get ..
        //	numbers of pages
       // console.log(pagenum);
        for (var i = 1; i <= pagenum; ) {
          // for each page append pagination li
          $(paginator + " #prev")
            .before(
              '<li class="page-item" data-page="' +
                i +
                '">\
                                    <span class="page-link">' +
                i++ +
                "</span>\
                                  </li>"
            )
            .show();
        } // end for i
      } // end if row count > max rows
      $(paginator +' [data-page="1"]').addClass("active"); // add active class to the first li
      $(paginator +" li").on("click", function (evt) {
        // on click each page
        evt.stopImmediatePropagation();
        evt.preventDefault();
        var pageNum = $(this).attr("data-page"); // get it's number
        //
        var maxRows =parseInt($(maxRow).val());

        if (pageNum == "prev") {
          if (lastPage == 1) {
            return;
          }
          pageNum = --lastPage;
        }
        if (pageNum == "next") {
          if (lastPage == $(paginator +" li").length - 2) {
            return;
          }
          pageNum = ++lastPage;
        }

        lastPage = pageNum;
        var trIndex = 0; // reset tr counter
        $(paginator + " li").removeClass("active"); // remove active class from all li
        $(paginator +' [data-page="' + lastPage + '"]').addClass(
          "active"
        ); // add active class to the clicked
        // $(this).addClass('active');					// add active class to the clicked
        reelHistorylimitPagging(paginator);
        $(table + " tbody tr.reel_history_tr.rowTrue").each(function () {
          // each tr in table not the header
          trIndex++; // tr index counter
          // if tr index gt maxRows*pageNum or lt maxRows*pageNum-maxRows fade if out
          if (
            trIndex > maxRows * pageNum ||
            trIndex <= maxRows * pageNum - maxRows
          ) {
            $(this).hide();
          } else {
            $(this).show();
          } //else fade in
        }); // end of for each tr in table
      }); // end of on click pagination list
      reelHistorylimitPagging(paginator);
    })
    .val(10)
    .change();

  // end of on select change

  // END OF PAGINATION
}

function reelHistorylimitPagging(paginator) {

  // alert($('.pagination li').length)
  if ($(paginator+ " li").length > 7) {
    if ($(paginator+ " li.active").attr("data-page") <= 3) {
      $(paginator+ " li:gt(5)").hide();
      $(paginator+ " li:lt(5)").show();
      $(paginator+ ' [data-page="next"]').show();
    }
    if ($(paginator+ " li.active").attr("data-page") > 3) {
      $(paginator+ " li:gt(0)").hide();
      $(paginator+ ' [data-page="next"]').show();
      for (
        let i =
          parseInt($(paginator+ " li.active").attr("data-page")) - 2;
        i <= parseInt($(paginator+ " li.active").attr("data-page")) + 2;
        i++
      ) {
        $(paginator+ ' [data-page="' + i + '"]').show();
      }
    }
  }
}
