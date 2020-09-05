
const uploadBtn = document.querySelector('.upload-btn');
const inputImg = document.querySelector('#input-img');

function formSend() {
    var formData = new FormData();

    const image = document.getElementById('image').files[0]
    formData.append("image", image);

    $.ajax({
        url:'/transform', // 요청 할 주소
        type: 'POST',
        enctype: 'multipart/form-data',
        processData : false,
        contentType: false,
        data: formData
    }).done(function(data) {
        if(typeof data == "string"){

        }
        for(let i=0; i<3; i++){
            let container = "img.con" + String((i+2));
            document.querySelector(container).setAttribute("src", data[i]);
        }
    }).fail(function (error) {
    });
}

function setThumbnail(event) { 
    var reader = new FileReader(); 
    reader.onload = function(event) { 
        document.querySelector("img.con1").setAttribute("src", event.target.result);
    }; 
    reader.readAsDataURL(event.target.files[0]); 
}
 


