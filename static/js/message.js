const grpslug = JSON.parse(document.getElementById('grpslug').textContent)
console.log(grpslug)
ws = new WebSocket('ws://localhost:8000/chat/' + String(grpslug)+'/')
ws.onopen = function(event){
    console.log("Connection opens",event)
    }
ws.onmessage = function(event){
    data = JSON.parse(event.data)
    if(data.action==='add'){
        time=getTime(data.timestamp)
        data.timestamp = {}
        data.timestamp.time = time
    // structure_message
    message_element = structure_message(data)
    document.getElementById('chat-box').innerHTML+=message_element
    // send to frontend 
    }
    else if(data.action==='delete'){
        console.log('removed from frontend also now')
        $('#chat-id-'+data.id).remove()
    }
    else if(data.action==='edit'){
        time=getTime(data.timestamp)
        data.timestamp = {}
        data.timestamp.time = time

        message_element = structure_message(data)
        console.log(data.id)
        console.log($('#chat-id-'+data.id).html())
        $('#chat-id-'+data.id).replaceWith(message_element)
        console.log($('#chat-id-'+data.id))
        $('.edit-msg').attr('class','btn msg-send')
    }
    

}
$(document).on("click",".forward-msg",function(){
    
})
ws.onerror = function(event){
    console.log("Error occurred: ",event)
}

ws.onclose = function(event){
    console.log("Connection Closed: ",event)
}
// add message realtime
$(document).on("click",'.msg-send',function(event){ 

    console.log("msg-send")
    reply_id = $(this).attr('reply-id')
    console.log(reply_id)
    data = document.getElementsByClassName('emojionearea-editor')[0]
    const add_msg = JSON.stringify({'action':'add','msg': document.getElementById('msg').value,'reply_id':reply_id})    
    data.textContent = ''
    $('#msg-send').removeAttr('reply-id')
    ws.send(add_msg)
})

// delete message realtime
$(document).on("click",".del-msg",function(){
    console.log('delete button clicked')
    msg_id = $(this).attr('data-id')
    console.log(msg_id)
    const del_msg = JSON.stringify({'action':'delete','msg_id': msg_id})
    console.log(del_msg)
    ws.send(del_msg)
})
$(document).on("click",'.edit-btn',function(){
    console.log('fds')
    msg_id = $(this).attr('data-id')
    msg_send = $('.msg-send')
    msg_send.attr('data-id',msg_id)
    $('.emojionearea-editor').html($('#text-msg-'+msg_id).html())
    msg_send.attr('class','btn edit-msg')
})
// edit message realtime 
$(document).on("click",".edit-msg",function(){
    msg_id = $('.edit-msg').attr('data-id')
    console.log(msg_id)
    data = document.getElementsByClassName('emojionearea-editor')[0]
    const add_msg = JSON.stringify({'action':'edit','msg': document.getElementById('msg').value,'msg_id':msg_id})
    data.textContent = ''
    ws.send(add_msg)
    
})
// reply message realtime
$(document).on("click",".reply-btn",function(){
    reply_id = $(this).attr('data-id')
    $('.msg-send').attr('reply-id',reply_id)
    reply_id_msg= $('#text-msg-'+reply_id).html()
    console.log(reply_id_msg)
    $('#reply-to').html(reply_id_msg)
    
})
function structure_message(data){
    let message_element
    username = JSON.parse(document.getElementById('user').textContent)
    message_element = `
    <div class="chat-message-right pb-4">
                                <div>
                                    <img src="${data.send_by.img}" class="rounded-circle mr-1" alt="${data.send_by.user.username}" width="40" height="40">
                                    <div class="text-muted small text-nowrap mt-2">${data.timestamp.time}</div>
                                </div>
    `
    if (username==data.send_by.user.username)
    {
        message_element+=`
        <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
        <div class="font-weight-bold mb-1">You</div>
        `
    }
    else{
        message_element+=`
        <div class="flex-shrink-1 bg-primary text-light rounded py-2 px-3 mr-3">
        <div class="font-weight-bold mb-1">${data.send_by.user.username}</div>
        `
    }
    message_element+=`
    ${data.message}
    </div>
    </div>
    `
    return message_element
   
    
}

$(document).ready(function() {
    $("#msg").emojioneArea();
  });
$(document).on("change",'#upload-doc',function(){
   let name = document.getElementById('upload-doc').files.item(0).name
   $('#selected-doc').html(name)
   $('.msg-send').attr('class','btn doc-send')
})

function getTime(timestamp){
    //let year = new Date(datetime).getFullYear();
    //let month = new Date(datetime).getMonth() + 1; // Add 1 to the month value to get the month in the standard format
    //let day = new Date(datetime).getDate();
    let hour = new Date(timestamp).getHours();
    let minute = new Date(timestamp).getMinutes();
    var ampm = "a. m.";
    if (hour >= 12)
    {
    ampm = "p. m.";
    hour = hour - 12;
    }
    return hour+':'+minute +' '+ampm
}
