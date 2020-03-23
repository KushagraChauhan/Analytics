/**
 * @fileoverview analytics.js
 * @author kushagra chauhan (kushagra_sc@yahoo.in)
 */
klayer = []
//Instead of datalayer, named it as klayer

//Basic idea---
/**
*When the user clicks on an image, the 'alt' attribute of the image which contains the subcategory
*of the item be sent to the server with some additional info about the user.
*/

//function summary
/**
*clickfunction: get the data and push it to the klayer
*sendData function: send the data to the server
*At present, I am using AJAX calls to send the data
*/

// Using callbacks to sequence the functions i.e.
// only after the clickfuntion(), sendData() function should work
function clickfunction(callback){

/**
* Using DOM Manipulations, I traverse through all the nodes
* which have a link associated with them.
*/
  document.addEventListener("click", function(e) {
    var a = e.target.closest("a[href]");
/**
* After the first Traversal, I traverse to the 'img' tag
* From there, I get the 'alt' attribute of the image.
*/
    if (a) {
  	   var img = e.target.closest("img[alt]")
  	   var alt = img.getAttribute("alt")
    }
/**
* From here-on, I get other details about the user such as
* Date, Time, platform, url, referrer, height and width of the device.
*/
    var d = new Date();
    var date = d.toISOString().slice(0,10);
    var time = d.toLocaleTimeString();
    var img = new Image;
    img.width = img.height = "1px";// Make an image of 1px
    var res = window.navigator;
    var data = {};
    var _plugins = {};
    data.date = date;
    data.time = time;
    data.url = window.location.href;
    data.ref = document.referrer;
    data.nav = res;
    data.subcategory = alt;
    data.width = window.screen.width;
    data.height = window.screen.height;
    data.platform = navigator.platform;
    data.history = history.length;
    //Store all the data in the image using dataset.stats
    img.dataset.stats = JSON.stringify(data);
/**
    Not using the push method as of datalayer
    As the method is not supported with common arrays
    Created my own way to push into the klayer
    in the form of Key:Value pair
*/
    var singleObj = {}
    singleObj['data'] = img.dataset.stats;
    klayer.push(singleObj);

  });
  return callback(function(){
     console.log("sendData finished.");
     return true;
   });
}
console.log(klayer)
//Send the data to the server
function sendData(callback){
//local server
  var server = "http://127.0.0.1:5000";
  console.log("sending the data to the flask app")
  var send = {};
  //send the datalayer
  function send_img(){
    send = klayer;
    console.log('-------hello-------');
  }

  //console.log("sending the data to the flask app")
  $(function() {
      $('img').click(function() {
        var appdir='/tracker';
        var send_msg = "<p>Sending request</p>";
        var received_msg = "<p>Details sent </p>";
        send_img();
        // console.log(received_msg);
        $('#message').html(send_msg);
        $.ajax({
            type: "POST",
            url:server+appdir,
            data: send,
            dataType: 'json'
        }).done(function(data) {
          console.log(data);
          $('#n3').val(data['img']);
          $('#message').html(received_msg);
        });
      });//72.167.20.118
    });
     return callback();
}
clickfunction(sendData);
