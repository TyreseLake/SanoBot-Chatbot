const host = location.hostname;

document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("input")
    inputField.addEventListener("keydown", function(e) {
      if (e.code === "Enter") {
        e.preventDefault();
        sendText();
      }
    });
});

async function sendText(){
  let input = document.getElementById("input")
  let value = input.value.trim();
  if(value!=""){
    input.disabled = true;
    await outputUser(value)
    await outputBot(value)
    input.disabled = false;
  }
  input.value = "";
}

async function outputUser(value){
  const chatbox = document.getElementById("chatbox");

  let usertextcontainer = document.createElement("div");
  usertextcontainer.className = "usertextcontainer";

  let usertext = document.createElement("div");
  usertext.className = "usertext";

  usertext.innerHTML = `${value}`;

  usertextcontainer.appendChild(usertext);
  chatbox.appendChild(usertextcontainer);

  chatbox.scrollTop = chatbox.scrollHeight;
}

async function outputBot(value){
  url = "/botlink"

  let data = {
    message: value
  }

  result = await postData(url, data);

  const chatbox = document.getElementById("chatbox");

  let bottextcontainer = document.createElement("div");
  bottextcontainer.className = "bottextcontainer";

  let botimage = document.createElement("img")
  botimage.src = "/static/BotUser.png"

  let bottext = document.createElement("div");
  bottext.className = "bottext";

  bottext.innerHTML = result;

  bottextcontainer.appendChild(botimage);
  bottextcontainer.appendChild(bottext);
  chatbox.appendChild(bottextcontainer);

  chatbox.scrollTop = chatbox.scrollHeight;
}

async function postData(url, data){
  try{
    let response = await fetch(
      url,
      {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'Content-Type' : 'application/json'}
      },
    );

    let result = await response.text();
    return result;
  }catch(error){
    console.log(error);
  }
}