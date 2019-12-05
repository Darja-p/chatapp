const loadedMessages = new Set();
let currentChat = null;
let userID = null;

const displayMessage = (message) => {

    let messageWrap = document.createElement('div')
    messageWrap.classList.add('message-wrap');

    let message_in_chat = document.createElement('div')
    if (message.sender_id == userID) {
        message_in_chat.classList.add('message','out');
      }else {message_in_chat.classList.add('message','in');
        let newMessageSender = document.createElement('p')
        newMessageSender.classList.add('mssg-sender');
        newMessageSender.innerHTML = message.sender_name
        message_in_chat.appendChild(newMessageSender)
    }

    let newMessage = document.createElement('p')
    newMessage.classList.add('mssg');
    newMessage.innerHTML = message.body
    message_in_chat.appendChild(newMessage)

    if (message.attachment != null) {
        let newPicture = document.createElement('img')
        // newPicture.classList.add('mssg');
        newPicture.height = 80; 
        newPicture.width = 150; 
        // let location = window.location.pathname;
        // var directoryPath = location.substring(0, location.lastIndexOf("/"));
        newPicture.src = `../static/pictures/${message.attachment}`;
        message_in_chat.appendChild(newPicture)

    }

    let newMessageTime = document.createElement('p')
    newMessageTime.classList.add('mssg-time');
    newMessageTime.innerHTML = message.date_created

    message_in_chat.appendChild(newMessageTime)

    messageWrap.appendChild(message_in_chat)

    const chatWrap = document.querySelector('#main-chat-wrap')
    chatWrap.appendChild(messageWrap)

}


const addMessages = (messages) => {
    for (const message of messages){
        if(!loadedMessages.has(message.id)) {
            loadedMessages.add(message.id);
            displayMessage(message)
        } 
    }
    // messages.forEach(post => addMessageOUT(post, user_id));
}

const retrieveMessages = (user_id, chat_id) => {
    const url = `/api/chats/${chat_id}/messages?user_id=${user_id}`
    fetch(url, {
        method: 'GET'
    }).then(res => res.json())
        .then(data => addMessages(data))
}





const convoClick = (event) => {
    const clicked = event.currentTarget;
    // populate form chat_id input
    const dataAttributes = clicked.dataset;
    userID= dataAttributes.user_id;
    currentChat = dataAttributes.chat_id;
    currentChatName = dataAttributes.chat_name
    document.querySelector('#sndr-chat_id').value = currentChat;
    deleteAll();
    //adding messages in current chat to the main chat
    retrieveMessages(userID,currentChat);
    //adding class active to the convo (first removing from the eiting one)
    let conversationActive = document.querySelector(".convo.active");
    console.log(conversationActive)
    if(conversationActive !== null) {
        conversationActive.classList.remove('active');
    }
    addActive(clicked);
    
}

setInterval (() => {
    if (currentChat !== null && userID !== null){
        retrieveMessages(userID, currentChat)  }
        },2000)
        

const deleteAll = () => {
    // clearing all the messages in a main chat to reload messages
    loadedMessages.clear();
    const chatWrap = document.querySelector('#main-chat-wrap')
    chatWrap.innerHTML = ""
}

const conversationElement = document.getElementsByClassName("convo");

for (let i=0; i < conversationElement.length; i++) {
    conversationElement[i].addEventListener('click', convoClick, false);
}

const addActive = (activeElement) => {
    // function adds active to the one which was clicked on
    activeElement.classList.add('active')
    deleteUsers()
    showUsers()
}

const deleteUsers = () => {
    const usersWrap = document.querySelector('#contact-header')
    usersWrap.innerHTML = ""
}


const showUsers = () => {
    if (currentChat !== null){
    const url = `/api/chats/${currentChat}/users`
    fetch(url, {
        method:'GET',})
        .then(res => res.json())
        .then(data => addNamesImages(data))
    }
}

const addNamesImages = (users) => {
    const usersHeader = document.querySelector('#contact-header')
    for (const user of users){

    let userPicture = document.createElement('div')
    userPicture.classList.add('head-img-wrap');

    let userPictureFile = document.createElement('img')
    userPictureFile.setAttribute("id", "user-image");
    userPictureFile.classList.add("icon-img")
    if (user.image.includes("google")) {
        userPictureFile.setAttribute("src",`${user.image}`)
    }
    else {
        userPictureFile.setAttribute("src",`/static/images/profilep/${user.image}`)
    }   
    userPicture.appendChild(userPictureFile)

    let userinChat = document.createElement('div')
    userinChat.classList.add('phone-number');

    let usersinChatName = document.createElement('p')
    usersinChatName.setAttribute("id", "sender-name");
    usersinChatName.innerHTML = user.name

    userinChat.appendChild(usersinChatName)

    usersHeader.appendChild(userPicture)
    usersHeader.appendChild(userinChat)
    }
}


    
const submitNewMessage = () => {
    // let addedMessage = document.getElementById('new-message-form').value
    const addedMessage=document.querySelector('#new-message').value;
    const chat_id = document.querySelector('#sndr-chat_id').value;
    const user_id = document.querySelector('#sndr-name').value;
    // const chat_id = currentChat.chat_id;
    // const user_id = currentChat.user_id
    const post_data= {
        'body': addedMessage,
        'chat': chat_id,
        'sender_id' : user_id}
    const url = `/api/chats/${chat_id}/messages?user_id=${user_id}`
    fetch(url, {
        method:'POST',
        headers : {
            'Content-type':'application/json'
    },
        body:JSON.stringify(post_data)
    }).then(res => res.json())
        .then(data => {
            // displaying message in the main window and adding message to the set of loaded message
            displayMessage(data)
            loadedMessages.add(data.id);
            // rewriting new message with emty string
            document.querySelector("#new-message").value = " "
            // updating last message in a chat in the side bar on a left
            document.querySelector(`div.convo[data-chat_id="${chat_id}"] p.mssg`).innerHTML = data.body
            })
        }
        
const deleteChat = () => {
    if (currentChat !== null){
        var okToRefresh = confirm(`Do you really want to delete the chat ${currentChatName}?`);
        if (okToRefresh){
            console.log(currentChat)
    const url = `/api/chats/${currentChat}`
    fetch(url, {
        method:'DELETE',
        }) .then (loadDiv())
    }}
}

const loadDiv = () => {
    // console.log(document.querySelector('#convo-wrap'))
    // location.reload(true)
    setTimeout(function () {
            location.reload()
        }, 100);
    }

const addUser = () => {
    if (currentChat !== null){
    const user_add=document.querySelector('#email-input').value;
    const url = `/api/chats/${currentChat}?user=${user_add}`
    fetch(url, {
        method:'POST',
    }).then (closeDropdown())
    .then(loadDiv())
}
    else {
        alert("Please click on a chat first")
        ;}
}


const realBtn = document.getElementById("picture-upload");

const attachImage = () => {
    realBtn.click();
}

realBtn.addEventListener("change", function() {
    if (realBtn.files[0]) {
        let file = document.getElementById("picture-upload").files[0];
        console.log(file)
        console.log(file.type)  
         // Check the file type.
        if (file.type.match('image.*')) {  
            let formData = new FormData();
            formData.append("file", file, file.name);
// fetch('/upload/image', {method: "POST", body: formData});
// let user = {name:'john', age:34} in this way: formData.append("user", JSON.stringify(user));
        // var img = document.createElement("img");
        // img.src = realBtn.value; 
        // img.height = 50; 
        // img.width = 100; 
    const addedMessageImage = ""      
    const chat_id_i = currentChat;
    const user_id_i = userID;
    let post = {body: "", chat: chat_id_i, sender_id: user_id_i }
    formData.append('post', JSON.stringify(post))
    // formData.append ('chat', JSON.stringify(chat_id_i))
    // formData.append ('sender_id', JSON.stringify(user_id_i))
    const url = `/api/chats/${chat_id_i}/upload_image?user_id=${user_id_i}`
    console.log(formData);
    console.log(formData.get('file'));
    console.log(formData.get('post'));
    fetch(url, {
        method:'POST',
        body: formData
    }).then (res => res.json()
       .then(data => {
    //  displaying message in the main window and adding message to the set of loaded message
    console.log(data)
        displayMessage(data)
        loadedMessages.add(data.id);
            // // rewriting new message with emty string
            // document.querySelector("#new-message").value = " "
            // // updating last message in a chat in the side bar on a left
            // document.querySelector(`div.convo[data-chat_id="${chat_id}"] p.mssg`).innerHTML = data.body
            })
    )}}})


        //   //optionally set a css class on the image
        //   var class_name = "foo";
        //   img.setAttribute("class", class_name);




/* When the user clicks on the button with dropdown,
toggle between hiding and showing the dropdown content */
const showDropdown = () => {
    document.getElementById("myDropdown").classList.toggle("show");
    // document.querySelector("myDropdown").classList.add("show");
  }

  const closeDropdown = () => {
    document.getElementById("myDropdown").classList.remove("show");
    // document.querySelector("myDropdown").classList.add("show");
  }


// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    // if (!event.target.matches('.dropbtn')) {
    if (!event.target.id == 'drop-btn') {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

  function hover(element) {
    element.setAttribute('src', 'static/images/1x/btn_google_signin_dark_focus_web.png');
  }
  
  function unhover(element) {
    element.setAttribute('src', 'static/images/1x/btn_google_signin_dark_normal_web.png');
  }