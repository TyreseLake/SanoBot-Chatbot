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
    await outputBot()
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

async function outputBot(){
  const chatbox = document.getElementById("chatbox");

  let bottextcontainer = document.createElement("div");
  bottextcontainer.className = "bottextcontainer";

  let botimage = document.createElement("img")
  botimage.src = "/static/BotUser.png"

  let bottext = document.createElement("div");
  bottext.className = "bottext";

  bottext.innerHTML = `Tell me more big boy!`;

  bottextcontainer.appendChild(botimage);
  bottextcontainer.appendChild(bottext);
  chatbox.appendChild(bottextcontainer);

  chatbox.scrollTop = chatbox.scrollHeight;
}