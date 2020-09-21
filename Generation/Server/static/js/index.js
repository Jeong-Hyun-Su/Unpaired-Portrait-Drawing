
const uploadBtn = document.querySelector('.upload-btn');
const inputImg = document.querySelector('#input-img');

function formSend() {
    let formData = new FormData();

    // Image, Version 선택
    const image = document.getElementById('image').files[0];
    let style = document.getElementById('style');
    style = style.options[style.selectedIndex].value;

    if(style == "" || style == ' '){
        alert("Choose the Version!");
        return;
    }

    if(style == "Style 1"){ style = "1-0-0" }
    else if(style == "Style 2"){ style = "0-1-0" }
    else if(style == "Style 3"){ style = "0-0-1" }

    formData.append("image", image);
    formData.append("style", style);
    
    fetch(
        '/transform',
        {
            method: 'POST',
            body: formData,
        }
    )
    .then(response => {
        if ( response.status == 200){
            return response
        }
        else{
            throw Error("transform error")
        }
    })
    .then(response => response.blob())
    .then(blob => URL.createObjectURL(blob))
    .then(imageURL => {
        document.querySelector("img.contain").setAttribute("src", imageURL);
    })
    .catch(e =>{
    })
}

function setThumbnail(event) { 
    var reader = new FileReader(); 
    reader.onload = function(event) { 
        document.querySelector("img.input-img").setAttribute("src", event.target.result);
        document.querySelector("img.contain").setAttribute("src", "../static/show/white.png");
    }; 
    reader.readAsDataURL(event.target.files[0]); 
}

function setExample(event) { 
    let style = document.getElementById('style');
    style = style.options[style.selectedIndex].value;

    let img = "../static/show/";

    if(style == "Style 1"){ img += "woman_fake1.png"; }
    else if(style == "Style 2"){ img += "woman_fake2.png"}
    else if(style == "Style 3"){ img += "woman_fake3.png"}
    else{ img += "white.png"; }

    document.querySelector("img.contain").setAttribute("src", img);
}
 


