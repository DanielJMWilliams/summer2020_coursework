document.addEventListener('DOMContentLoaded', function(){
    importBtn = document.querySelector('#import-btn');
    importBtn.onclick = function(){
        importBtn.classList.remove("btn-success");
        importBtn.classList.add("btn-warning");
        //importBtn.innerHTML = "importing...";
        document.querySelector('#btn-info').innerHTML = "importing";

        importLibrary(0);

        return false;
    };
});

function importLibrary(offset){
    const request = new XMLHttpRequest();
    request.open('GET',"importLikedSongs/"+offset.toString());
    //console.log(request);

    // Include csrf token in header so Django will accept the request
    const header =  "X-CSRFToken";
    const token = getCookie('csrftoken'); //Using the js-cookies library
    request.setRequestHeader(header, token);

    // Send request
    request.send(null);

    //console.log("request sent");

    request.onload = function(){
        //console.log("request loaded");
        //console.log(request.responseText);
        const data = JSON.parse(request.responseText);

        for(i=0;i<data.tracks.length;i++){
            track = data.tracks[i];
            dt = $('#songs').DataTable();
            dt.row.add([
                dt.rows().count()+1,
                track.name,
                track.artists,
                track.bpm,
            ]).draw();
        }

        //otherwise there are no more tracks to import
        if(data.tracks.length!=0){
            progress = (Math.round((data.offset/data.numSongs)*100)).toString() +"%"
            document.querySelector('#btn-info').innerHTML = "importing "+progress;
            importLibrary(data.offset);
        }
        else{
            importBtn.classList.remove("btn-warning");
            importBtn.classList.add("btn-success");
            document.querySelector('#btn-info').innerHTML = "Success";
            document.querySelector('#numImported').innerHTML=data.numSongs;
            document.querySelector('#percentageImported').innerHTML="100";
        }

    };
}