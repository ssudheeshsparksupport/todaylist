$(document).ready(function() {
    $("form").on("submit", function(e) {
        e.preventDefault();
    });
    loadItems();

    function find_hashtag(text) {
        if (text.indexOf('#') != -1) {
            sub = text.split('#')[1]
            if (sub.indexOf(' ') != -1) {
                hash = sub.split(' ')[0]
            } else {
                hash = sub;
            }
            return hash
        }
        return null
    }
    $('#save').on('keypress', function(e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        task = $("input").val()
        if (code == 13 && task.length > 0) {
            e.preventDefault();
            if (task.indexOf('/free')!=-1 ||task.indexOf('/pause')!=-1){
              $.get("/app/free/").done(function(data){
                console.log('You are now free!!');
                $("input").val("");
              });
            }
            else if(task.indexOf('/resume')!=-1){
              $("input").val("");
              $.get("/app/resume/").done(function(data){
                if(data.success==true){
                  put_to_feed(data.task)
                }
              });
            }
            else{
              if (task.indexOf('#') != -1) {
                sub = task.split('#')[1]
                if (sub.indexOf(' ') != -1) {
                    t_team = sub.split(' ')[0]
                } else {
                    t_team = sub;
                }
                input = {
                    "title": $("input").val(),
                    "team": t_team
                }
            } else {
                input = {
                    "title": $("input").val(),
                }
            }

            var data = {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'data': JSON.stringify(input)
            }
            jQuery.post("/app/task/create/", data,
                function(data) {
                    $("input").val("");
                    $(format_feed(data.data)).hide().prependTo('#feeds').slideDown("slow");
                });
            }
            
        }
    });
});
function put_to_feed(data){
  $(format_feed(data)).hide().prependTo('#feeds').slideDown("slow");
}
$("#teamselect").change(function() {
    window.team = $("#teamselect").val()
    $('#feeds .feeds').remove()
    loadItems()
});


var $loading = $('#loadingDiv').hide();
$(document)
    .ajaxStart(function() {
        $loading.show();
    })
    .ajaxStop(function() {
        $loading.hide();
    });

function format_feed(feed) {
    feed.title = feed.title.replace(/(\#\w+)/g,"<span class=\"hashtag\">$1</span>")
    return '<div class="row feeds">' + '<div class="col-sm-1 col-md-1 imagebox">' + '<img class="chat" src="' + feed.image + '" alt="Chat"><p class="username">'+feed.username+'</p></div>' + '<div class="col-sm-11 col-md-11">' + '<div class="feed">' + '<span class="right timesfor date">' + momentdata(feed.create_time.$date) + '</span>'  + '<p>'+ feed.title + '</p>' + '</div>' + '</div>' + '</div>'
}

var team = "all"
var url = '/app/feed/'
var has_next
var next
var nexturl = '/app/feed/'

    function loadItems(loadObject) {
        var dataurl = window.url + '?team=' + window.team
        if (typeof loadObject != 'undefined') {
            if (typeof loadObject.next != 'undefined')
                dataurl += "&page=" + loadObject.next
        }
        $.ajax({
            url: dataurl,
            cache: false,
            dataType: 'json',
            success: function(result) {
                console.log(result)
                window.has_next = result.has_next
                window.next = result.next_page
                for (var k in result.feed) {
                    feed = result.feed[k]
                    $("#feeds").append(format_feed(feed))
                }
            }
        });
    }


    function momentdata(data) {
        return moment.utc(data).fromNow();
    }


$(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
        if (window.has_next) {
            loadItems({
                next: window.next
            })
        }
    }
});
