var dragger = document.getElementById("dragger");
var dragger_text = document.getElementById("dragger_text");
var browseFileBtn = document.getElementById("browseFileBtn");
var fileSelectorInput = document.getElementById("fileSelectorInput");
var filename = document.getElementById("filename");

const browseFileMonitor = ()=>{
    fileSelectorInput.value = "";
    fileSelectorInput.click();
}

fileSelectorInput.addEventListener("change", function(e){
    file = this.files[0];
    uploadFileMonitor(file);
});

dragger.addEventListener("dragover", (e)=>{
    e.preventDefault();
    dragger_text.textContent = "Release to upload image";
});

dragger.addEventListener("dragleave", ()=>{
    dragger_text.textContent = "Drag and drop file";
});

dragger.addEventListener("drop", (e)=>{
    e.preventDefault();
    file = e.dataTransfer.files[0];
    uploadFileMonitor(file);
});

const deleteHandler = ()=>{
    const initial = ' <div id="dragger"> <div class="icon"><i class="fa-solid fa-images"></i></div> <h2 id="dragger_text"> Drag and drop file </h2><h3> OR </h3><Button class="browseFileBtn" onclick="browseFileMonitor" > Browse File </Button><input type="file" hidden id="fileSelectorInput" /></div>';
    dragger.innerHTML = initial;
    dragger.classList('active');
    filename.innerHTML = "";
}

const uploadFileMonitor = (file)=>{
    const validatedExtensions = ['image/jpeg', 'image/jpg', 'image/png', 'image/x-portable-graymap',];
    alert(file.type);
    if (validatedExtensions.includes(file.type)){
        const fileReader = new FileReader();

        fileReader.readAsDataURL(file);

        fileReader.onload = ()=>{
            const fileURL = fileReader.result;
            
            //const imageTag = '<img src="'+fileURL+'"alt="" />';
            const imageTag = '<img src="'+fileURL+'"alt="" />';
            dragger.innerHTML = imageTag;
            console.log(fileURL);
            //const imageDetails = '<p>'+file.name.split(',')[0]+'</p><i id = "BtnDelete" class="fa-solid fa-trash-can" onclick="deleteHandler()"></i>'
            const imageDetails = '<p>'+file.name.split(',')[0]+'</p> <Button id = "BtnDelete" class="fa-solid fa-trash-can" onclick="deleteHandler()" > </Button>'
            filename.innerHTML = imageDetails;
        }
        dragger.classList.add('active');

    }
}


