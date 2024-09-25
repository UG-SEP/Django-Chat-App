const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = 'en-US';
recognition.interimResults = false;
$(document).on("click",'#mic-on',function(){ 
    recognition.start();
    recognition.onstart = function(){
        $('#mic-off').css("display","inline")
        $('#mic-on').css("display","none")
    }
    recognition.onend = function(){
        $('#mic-on').css("display","inline")
        $('#mic-off').css("display","none")
    }
    recognition.onresult = (event) => {
      const text = event.results[event.resultIndex][0].transcript;
      console.log(text)
      previous_msg = $('.emojionearea-editor').html()
      $('.emojionearea-editor').html(previous_msg+' '+text)
    }
  })
  $(document).on("click",'#mic-off',function(){
    recognition.stop();
  })