document.addEventListener('DOMContentLoaded', function(){
    durationInput = document.querySelector('#duration');
    numberOfSongsInput = document.querySelector('#number-of-songs');
    durationInput.addEventListener('input', function(){
        if(durationInput.value!=""){
            numberOfSongsInput.disabled=true;
            numberOfSongsInput.style.backgroundColor="grey";
            numberOfSongsInput.style.opacity="0.2";
        }
        else{
            numberOfSongsInput.disabled=false;
            numberOfSongsInput.style.backgroundColor="white";
            numberOfSongsInput.style.opacity="1";
        }
    });
    numberOfSongsInput.addEventListener('input', function(){
        if(numberOfSongsInput.value!=""){
            durationInput.disabled=true;
            durationInput.style.backgroundColor="grey";
            durationInput.style.opacity="0.2";
        }
        else{
            durationInput.disabled=false;
            durationInput.style.backgroundColor="white";
            durationInput.style.opacity="1";
        }
    });

    var lastTimeClicked = 0;
    var timeBetweenClicks = []
    document.querySelectorAll('.tap').forEach( function(btn){
        btn.onclick = function(){
            d = new Date();
            var t = d.getTime();
            dt = t-lastTimeClicked
            if(dt>2000){
                //reset array if pause too long
                timeBetweenClicks = []
            }
            else{
                timeBetweenClicks.push(dt);
                console.log(timeBetweenClicks);
                averageTimeBetweenClicks = calculateAverage(timeBetweenClicks);
                bpm=60/(averageTimeBetweenClicks/1000);
                document.querySelector(btn.dataset.target).value = Math.round(bpm);
            }
            
            lastTimeClicked=t
            return false;
        };
    });
});

function calculateAverage(array){
    total = 0;
    for(let i=0;i<array.length;i++){
        total+=array[i];
    }
    average = total/array.length;

    return average;

}