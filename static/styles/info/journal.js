function setcolSpan(num, wd)
{
    switch(num) {
        case 0:
        var element = document.getElementById('jan');
        element.setAttribute("colspan", wd)
        break;
        case 1:
        var element = document.getElementById('feb');
        element.setAttribute("colspan", wd)
        break;
         case 2:
        var element = document.getElementById('mar');
        element.setAttribute("colspan", wd)
        break;
         case 3:
        var element = document.getElementById('apr');
        element.setAttribute("colspan", wd)
        break;
         case 4:
        var element = document.getElementById('may');
        element.setAttribute("colspan", wd)
        break;
         case 8:
        var element = document.getElementById('sep');
        element.setAttribute("colspan", wd)
        break;
         case 9:
        var element = document.getElementById('oct');
        element.setAttribute("colspan", wd)
        break;
         case 10:
        var element = document.getElementById('nov');
        element.setAttribute("colspan", wd)
        break;
         case 11:
        var element = document.getElementById('dec');
        element.setAttribute("colspan", wd)
        break;
      }
}

function isWorkingDay(date) {
    return date.getDay() !== 0;
  }
  
  
  function countWorkingDays(year, month) {
    var totalDays = new Date(year, month + 1, 0).getDate();
    var workingDays = 0; 
    
    for (var day = 1; day <= totalDays; day++) {
      var currentDate = new Date(year, month, day);
      if (isWorkingDay(currentDate)) {
        addCell(currentDate.getDate());
        workingDays++;
      }
    }
    return workingDays;
  }


  function addCell(i) {

    var table = document.getElementById("marks");
  
    var cell = document.createElement("th");

    cell.textContent = i; 
  
    var row = table.rows[2];
    row.appendChild(cell);
  }


  document.addEventListener('DOMContentLoaded', function() {

    var allWorkingDays = 0;
    var table = document.getElementById("marks");

    var currentDate = new Date();

    var currentMonth = currentDate.getMonth();

    var currentYear = currentDate.getFullYear();

    var nextYear = currentYear + 1;

    for(var month = 8; month < 12; ++month)
    {
        var workingDays = countWorkingDays(currentYear, month);

        setcolSpan(month, workingDays);

        allWorkingDays += workingDays;

    }

    if (currentMonth < 5)
    {
        for(var month = 0; month < 5; ++month)
        {
            var workingDays = countWorkingDays(currentYear, month);

            setcolSpan(month, workingDays);
            
            allWorkingDays += workingDays;

        }
    }

    else
    {
        for(var month = 0; month <= 5; ++month)
        {
            var workingDays = countWorkingDays(nextYear, month);

            setcolSpan(month, workingDays);

            allWorkingDays += workingDays;

        }
    }

    var header = document.getElementById("mheader");

    header.setAttribute("colspan", allWorkingDays);

  });
  