'use strict';

/* login
// Save Login Info in local storage 
const loginId = document.querySelector("#loginId");
const loginPw = document.querySelector("#loginPw");
const loginBtn = document.querySelector("#loginBtn");

const USERID_KEY="userId";
const USERPW_KEY="userPw";

function onLoginSubmit(e){
    e.preventDefault();

    const userId = loginId.value;
    localStorage.setItem(USERID_KEY, userId);

    const userPw = loginPw.value;
    localStorage.setItem(USERPW_KEY, userPw);

    location.href = "./index.html";
}

loginBtn.onclick=(e)=>{
    onLoginSubmit(e);
}


// Save Register Info in local storage 
const joinId = document.querySelector("#registerId");
const joinPw = document.querySelector("#registerPw");
const joinBtn = document.querySelector("#registerBtn");
const joinName = document.querySelector("#registerName");
const joinEmail = document.querySelector("#registerEmail");
const joinTel = document.querySelector("#registerTel");

const JOINID_KEY = "id";
const JOINPW_KEY = "pw";
const JOINNAME_KEY = 'name';
const JOINEMAIL_KEY = 'email';
const JOINTEL_KEY = 'tel';

function onRegisterSubmit(e){
    e.preventDefault();

    const joinId = joinId.value;
    localStorage.setItem(JOINID_KEY, joinId);

    const joinPw = joinPw.value;
    localStorage.setItem(JOINPW_KEY, joinPw);

    const joinName = joinName.value;
    localStorage.setItem(JOINNAME_KEY, joinName);

    const joinEmail = joinEmail.value;
    localStorage.setItem(JOINEMAIL_KEY, joinEmail);

    const joinTel = joinTel.value;
    localStorage.setItem(JOINTEL_KEY, joinTel);
}
*/