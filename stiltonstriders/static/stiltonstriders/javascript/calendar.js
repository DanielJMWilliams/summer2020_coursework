var selectedBtn;
document.addEventListener('DOMContentLoaded', function () {
    selectedBtn = document.querySelector('.day');

    addDayBtnFunctionality();

    var monthOffset = 0
    getMonth(monthOffset);
    document.querySelector('#offset-month-backwards').onclick = function () {
        monthOffset--;
        getMonth(monthOffset);
    }
    document.querySelector('#offset-month-forwards').onclick = function () {
        monthOffset++;
        getMonth(monthOffset);
    }

})

function getMonth(month) {
    //get pizza price from server
    const request = new XMLHttpRequest();
    request.open('POST', "getMonth");
    //console.log(request);

    // Include csrf token in header so Django will accept the request
    const header = "X-CSRFToken";
    const token = getCookie('csrftoken'); //Using the js-cookies library
    request.setRequestHeader(header, token);

    // Add data to send with request
    let data = new FormData();
    // TODO: year and month change
    data.append("month_offset", month);


    // Send request
    request.send(data);

    //console.log("request sent");

    request.onload = function () {
        //console.log("request loaded");
        //console.log(request.responseText);
        const data = JSON.parse(request.responseText);

        const weeks = data.weeks;

        document.querySelector("#month").innerHTML = data.month_name;
        document.querySelector("#month").dataset.month_num=data.month_num;
        document.querySelector("#year").innerHTML =  data.year;
        document.querySelector(".weeks").innerHTML="";
        const template = Handlebars.compile(document.querySelector('#week-template').innerHTML);
        for(i=0;i<weeks.length;i++){
            console.log(weeks[i])
            const content = template({ "days":  weeks[i], "race":true});
            document.querySelector(".weeks").innerHTML+=content;
        }
        selectedBtn = document.querySelector('.day');
        addDayBtnFunctionality();
        

    };
}

function addDayBtnFunctionality(){
    document.querySelectorAll('.day').forEach(function (dayBtn) {
        if(dayBtn.innerHTML!=""){
            dayBtn.onclick = function () {
                //deselect previous selection
                selectedBtn.style.backgroundColor = "#FFFFFF";
                selectedBtn = dayBtn;
                selectedBtn.style.backgroundColor = "#CCCCCC";
                document.querySelector('#selected-date').innerHTML = selectedBtn.innerHTML;
                day = selectedBtn.innerHTML;
                month = document.querySelector('#month').dataset.month_num;
                year = document.querySelector('#year').innerHTML;
                getEvents(day, month, year);
            };
        }
        else{
            dayBtn.style.backgroundColor = "#888888";
        }
    });
}


function getEvents(day, month, year) {

    //get pizza price from server
    const request = new XMLHttpRequest();
    request.open('POST', "getEvents");
    //console.log(request);

    // Include csrf token in header so Django will accept the request
    const header = "X-CSRFToken";
    const token = getCookie('csrftoken'); //Using the js-cookies library
    request.setRequestHeader(header, token);

    // Add data to send with request
    let data = new FormData();
    // TODO: year and month change
    data.append("year", year);
    data.append("month", month);
    data.append("day", day);
    //console.log(data);

    // Send request
    request.send(data);

    //console.log("request sent");

    request.onload = function () {
        //console.log("request loaded");
        console.log(request.responseText);
        const events = JSON.parse(request.responseText);
        document.querySelector("#events-list").innerHTML = "";
        for (i = 0; i < events.length; i++) {
            document.querySelector("#events-list").innerHTML += events[i].name
        }


    };
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}