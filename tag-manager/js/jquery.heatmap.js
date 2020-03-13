;(function($){
    "use strict"
    $.fn.heatmapElement = function(options){
        // Default options, changeable by the user via HTML
        var defaults = $.extend({
            count: 0,   // Sets the starting number for counting
            disableCount: false, // Enables/disables counting
            disableButton: false, // Enables/disables the button
            refreshSpeed: 300, // The refresh speed of the shown count number
            resize: 1, // Multiplies the heatmap's size with the given value
        }, options);

        var heatmapWidth = this.width();
        var heatmapHeight = this.height();

        // Creating the necessary elements for the heatmap
        var div = $("<div></div>");
        var counter = $("<p></p>");
        var canvas = $("<canvas></canvas>");
        if(!defaults.disableButton){
            var button = $("<button>Show/Hide Heatmap</button>");
        }
        var context = canvas[0].getContext("2d");
        var $this = $(this);
        var heatmap = construct();

        // Constructor funtion: Appends the created elements to their places
        // and contains the click functions
        function construct(){
            $("body").append(div);
            if(!defaults.disableButton){
                $("body").append(button);
            }
            $(div).append(counter);

            $(div).append(canvas);
            $(canvas).attr({'id': 'canvas'});
            canvas[0].width = heatmapWidth*defaults.resize;
            canvas[0].height = heatmapHeight*defaults.resize;
            $(canvas).css({"border":"1px solid black"});

            $(div).hide();

            return{
                leftClick: function(xCoor, yCoor){
                    context.beginPath();
                    context.strokeStyle = "green";
                    context.moveTo(xCoor, yCoor);
                    context.arc(xCoor+1, yCoor+1, 5,0,2 * Math.PI, );
                    context.fillStyle = "green"
                    context.fill()
                    context.stroke();
                },
                rightClick: function(xCoor, yCoor){
                    context.beginPath();
                    context.strokeStyle = "yellow";
                    context.moveTo(xCoor, yCoor);
                    context.arc(xCoor+1, yCoor+1, 5,0,2 * Math.PI, );
                    context.fillStyle = "yellow"
                    context.fill()
                    context.stroke();
                },
                toggleDiv: function(){
                    $(div).toggle();
                }
            }
        }
        if(!defaults.disableCount){
            setInterval(function(){$(counter).text("Total clicks on " + $this.prop("tagName") + " Element: " + defaults.count)},
                        defaults.refreshSpeed);
        }
        if(!defaults.disableButton){
            $(button).click(function(){
                heatmap.toggleDiv();
            });
        }
        // Gets the coordinates of the click and passes it to the appropriate function
        $($this).click(function(){
            var offset = $(this).offset();
            var x = (event.pageX - offset.left)*defaults.resize;
            var y = (event.pageY - offset.top)*defaults.resize;

            heatmap.leftClick(x, y);
            if(!defaults.disableCount){
                defaults.count += 1;
            }
        });
        $($this).contextmenu(function(){
            var offset = $(this).offset();
            var x = (event.pageX - offset.left)*defaults.resize;
            var y = (event.pageY - offset.top)*defaults.resize;

            heatmap.rightClick(x, y);
            if(!defaults.disableCount){
                defaults.count += 1;
            }
        });
        $('#canvas').click(function() {
        this.href = $('#canvas')[0].toDataURL();// Change here
        this.download = 'design.png';
        });
    };
})(jQuery);
