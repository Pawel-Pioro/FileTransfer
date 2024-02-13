document.addEventListener('DOMContentLoaded', function() {
    const btns = document.querySelectorAll('#deleteButton')
    btns.forEach(btn => {
        btn.addEventListener('click', function(){deleteUpload(btn.getAttribute("name"));});
    });
    // default
    myFiles();
});

function myFiles(){
    document.querySelector('#title').innerHTML = 'My Files';
    document.querySelector('#myFiles').style.display = 'block';
}

function upload(){
    document.querySelector('#title').innerHTML = 'Upload File';
    document.querySelector('#myFiles').style.display = 'none';
}

function deleteUpload(pk){
   fetch('delete',{
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            pk: pk
        })
    }).then(window.location.href = "/")
}