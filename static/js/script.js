socket = new WebSocket('ws://192.168.100.28:5678/');

console.log("Lol")

$(document).ready(function() {
    $(".bottle").click(function(event) {
        pos = $(event.target).attr("value");
        color = $("#color").val();
        $(event.target).css("background", color);
        msg = '{"pos": '+ pos+', "color": "'+ color + '"}'
        console.log(msg)
        socket.send(msg);
    });
});