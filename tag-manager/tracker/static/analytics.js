//Analytics.js

klayer = [{
  'name':'kush'
}]
document.addEventListener("click", function(e) {
    var a = e.target.closest("a[href]");
    if (a) {
        // The event passed through the element on its way to the document
	var img = e.target.closest("img[alt]")
	var alt = img.getAttribute("alt")
  }
  var d = new Date();
  var date = d.toISOString().slice(0,10);
  var time = d.toLocaleTimeString();
  var img = new Image;
  img.width = img.height = "1px";
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
  img.dataset.stats = JSON.stringify(data);
  klayer.push(img.dataset.stats)
  console.log(
    img.dataset.stats
  );
});
//Send the data to the server
  console.log("sending the data to the flask app")
  var server = "http://127.0.0.1:5000";
  //console.log("sending the data to the flask app")
  var send = {};

  function send_img(){
    send = img.dataset.stats;
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
