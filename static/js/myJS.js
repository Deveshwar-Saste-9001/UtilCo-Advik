function sideMenu(menuItem, link) {
    const menuItems = document.querySelectorAll(".side-menu-item");
    menuItems.forEach(item => {
        item.classList.remove("selected");
        item.classList.add("unselected");
    });
    menuItem.classList.add("selected");
    menuItem.classList.remove("unselected");
    window.location.href = link;

}

function handlePopup() {
    const closeBtn = document.querySelector(".initial-popup");
    closeBtn.style.visibilty = "hidden";
    closeBtn.style.display = "none";
}

function handleImageClick(imageLink, isDevice, isHome) {
    const imageView = document.getElementById("mainImage");
    const yellowView = document.getElementById("yellowView");
    const redView = document.getElementById("redView");
    const greenView = document.getElementById("greenView");
    imageView.src = imageLink;
    if (isHome){
        yellowView.style.display = "grid"
        redView.style.display = "grid"
        greenView.style.display = "grid"
    } else{
        yellowView.style.display = "none"
        redView.style.display = "none"
        greenView.style.display = "none"
    }
    const deviceIcon = document.getElementById('deviceiconid');
    if (isDevice) {
        deviceIcon.innerText = "Connected Devices"
    } else {
        deviceIcon.innerText = "No Devices";
    }
}

function handleDevicePopup() {
    const deviceIcon = document.getElementById('deviceiconid');
    const devicePop=document.getElementById('devicePopupid');
    const txt = deviceIcon.innerText;
    if (txt.localeCompare("No Devices")) {
        devicePop.style.display = 'grid';
    } if(txt.localeCompare("Connected Devices")){
        devicePop.style.display = 'none';
    }
}
function closeDevicePop(){
document.getElementById("devicePopupid").style.display='none'



}

function handleGraphPopup(show){
    if (show){
        document.getElementById("graphPopupID").style.display = "grid"
    }
    else{
        document.getElementById("graphPopupID").style.display = "none"
    }
    
}

