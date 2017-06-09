

var searchArr;

if(localStorage.search){

    searchArr= localStorage.search.split(",")
}else{

    searchArr = [];
}

MapSearchArr();


$("#btn").on("click", function(){
    var val = $("#inp").val();

    KillRepeat(val);

    localStorage.search = searchArr;

    MapSearchArr();
});


function MapSearchArr(){
    var tmpHtml = "";
    for (var i=0;i<searchArr.length;i++){
        tmpHtml += "<span>" + searchArr[i] + "</span> "
    }
    $("#keyname").html(tmpHtml);
}

function KillRepeat(val){
    var kill = 0;
    for (var i=0;i<searchArr.length;i++){
        if(val===searchArr[i]){
            kill ++;
        }
    }
    if(kill<1){
        searchArr.push(val);
    }
}

