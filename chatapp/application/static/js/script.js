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

    let newMessageTime = document.createElement('p')
    newMessageTime.classList.add('mssg-time');
    newMessageTime.innerHTML = message.date_created

    message_in_chat.appendChild(newMessage)
    message_in_chat.appendChild(newMessageTime)

    messageWrap.appendChild(message_in_chat)

    const chatWrap = document.querySelector('#main-chat-wrap')
    chatWrap.appendChild(messageWrap)

}


const addMessages = (messages) => {
    // let messages = mockAPI.conversations[0].messages;
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



const conversationElement = document.getElementsByClassName("convo");

const convoClick = (event) => {
    const clicked = event.currentTarget;
    // populate form chat_id input
    const dataAttributes = clicked.dataset;
    userID= dataAttributes.user_id;
    currentChat = dataAttributes.chat_id;
    document.querySelector('#sndr-chat_id').value = currentChat;
    deleteAll();
    //adding messages in current chat to the main chat
    retrieveMessages(userID,currentChat);
    //adding class active to the convo
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
    loadedMessages.clear();
    const chatWrap = document.querySelector('#main-chat-wrap')
    chatWrap.innerHTML = ""
}

for (let i=0; i < conversationElement.length; i++) {
    conversationElement[i].addEventListener('click', convoClick, false);
}

const addActive = (activeElement) => {
    // function removes active from all convo and then adds only to the one which was clicked on
    // if (!activeElement.classList.contains("active")){
    activeElement.classList.add('active')
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
            displayMessage(data)
            document.querySelector("#new-message").value = " "
            document.querySelector(`div.convo[data-chat_id="${chat_id}"] p.mssg`).innerHTML = data.body
            })
        }
        


        // const addedChat=document.querySelector('#new-message').value;
        // const chat_id = document.querySelector('#sndr-chat_id').value;
        // const user_id = document.querySelector('#sndr-name').value;
    // creating new chat when click on button  

// $('#exampleModal').modal()


// const popupShow = () => {
//         let modal=document.getElementById('exampleModal')
//         console.log(modal)
//         modal.style.display = "block";
//         }
// onclick="popupShow()"

// var modal = document.getElementById("myexampleModal");

// // Get the button that opens the modal
// var btn = document.getElementById("myBtn");

// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];

// // When the user clicks on the button, open the modal
// btn.onclick = function() {
//   modal.style.display = "block";
// }

// // When the user clicks on <span> (x), close the modal
// span.onclick = function() {
//   modal.style.display = "none";
// }

// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }