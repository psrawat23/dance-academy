// Function for search fiilter

function SearchFilter(SearchBoxId,tableID){

    const search = document.querySelector(SearchBoxId);
    search.addEventListener('keyup', () => {
      const value = search.value.toLowerCase();
      const rows = document.querySelectorAll(tableID +' tbody tr');
      rows.forEach(row => {
        const cells = row.children;
        let isMatching = false;
        for (let i = 0; i < cells.length; i++) {
          if (cells[i].textContent.toLowerCase().indexOf(value) !== -1) {
            isMatching = true;
            break;
          }
        }
        if (isMatching) {
          $(row).show()
    //    Assigning the rowTrue class to identify which row to show
          row.classList.add("rowTrue");
        } else {
  
            $(row).hide()
          row.classList.remove("rowTrue");
     
        }
      });
    
      
    //   Triggering an change event to make update in the pagination 
    // Select Row is the id of selectform in service_list page
    let element = document.getElementById("selectRow");
      element.dispatchEvent(new Event('change'));
    
    });
    
    }
    
    // function for select filter region
    
    function SelectFilter(selectBoxId,Column,tableId){
    
    const selectedValue=document.querySelector(selectBoxId);
    selectedValue.addEventListener('change',(event)=>{
    
    const value= event.target.value.toLowerCase();
    const rows = document.querySelectorAll(tableId + ' tbody tr');
    rows.forEach(row=>{
    
    
        const cells= row.children;
        let isMatching = false;
    
        for (let i = 0; i < cells.length; i++) {
          if ((cells[i].hasAttribute(Column) && value==cells[i].textContent.toLowerCase()) || (value=="all")) {
            isMatching = true;
            break;
          }
        }
        if (isMatching) {
          row.style.display = '';
          row.classList.add("rowTrue");
        } else {
          row.style.display = 'none';
    
          row.classList.remove("rowTrue");
        }
    
    
    });

     //   Triggering an change event to make update in the pagination 
    // Select Row is the id of selectform in service_list page
    let element = document.getElementById("selectRow");
      element.dispatchEvent(new Event('change'));
    
    
    
    });
    
    
    }
    