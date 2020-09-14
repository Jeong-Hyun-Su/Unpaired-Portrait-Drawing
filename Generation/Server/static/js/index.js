
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
 


