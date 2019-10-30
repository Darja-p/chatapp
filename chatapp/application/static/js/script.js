
const addMessageOUT = (post, user_id) => {

    let messageWrap = document.createElement('div')
    messageWrap.classList.add('message-wrap');

   
    let messageOut = document.createElement('div')
    if (post.sender_id == user_id) {
        messageOut.classList.add('message','out');
      }else {messageOut.classList.add('message','in');
    }

    let newMessage = document.createElement('p')
    newMessage.classList.add('mssg');
    newMessage.innerHTML = post.body

    let newMessageTime = document.createElement('p')
    newMessageTime.classList.add('mmssg-time');
    newMessageTime.innerHTML = post.date_created

    messageOut.appendChild(newMessage)
    messageOut.appendChild(newMessageTime)

    messageWrap.appendChild(messageOut)

    const chatWrap = document.querySelector('#main-chat-wrap')
    chatWrap.appendChild(messageWrap)
    console.log(messageWrap)

}

const addMessages = (messages,user_id) => {
    // let messages = mockAPI.conversations[0].messages;
    const chatWrap = document.querySelector('#main-chat-wrap')
    chatWrap.innerHTML = ""
    messages.forEach(post => addMessageOUT(post, user_id));
}

const retrieveMessages = (req_info) => {
    console.log(req_info.chat_id, req_info.user_id)
    var user_id = req_info.user_id;
    const url = `/api/chats/${req_info.chat_id}/messages?user_id=${req_info.user_id}`
    fetch(url, {
        method: 'GET'
    }).then(res => res.json())
        .then(data => addMessages(data,user_id))
}



const conversationElement = document.getElementsByClassName("convo");

const convoClick = (event) => {
    const clicked = event.currentTarget;
    // console.log(clicked.dataset)
    retrieveMessages(clicked.dataset);
}



for (let i=0; i < conversationElement.length; i++) {
    conversationElement[i].addEventListener('click', convoClick, false);
}



// var ele = /*Your Form Element*/;
// if(ele.addEventListener){
//     ele.addEventListener("submit", callback, false);  //Modern browsers
// }else if(ele.attachEvent){
//     ele.attachEvent('onsubmit', callback);            //Old IE
// }

// submitNewMessage()