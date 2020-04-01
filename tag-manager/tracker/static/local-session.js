/**
* This implements the sessions using localStorage.
* @author: Kushagra Chauhan
*/


window.localStorage.setItem("sessionID", "1");
window.localStorage.getItem("sessionID");
setTimeout(function(){localStorage.removeItem("sessionID");}, 1000*60*60);
