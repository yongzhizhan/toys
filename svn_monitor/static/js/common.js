$.extend({
    jpost: function(url, body) {
        return $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(body),
            contentType: "application/json",
            dataType: 'json'
        });
    }
});

var SVNMonitor = function(options){
    var _options = options || {};
    var _export = {
        list: function(success){
            $.get("/list", function(data){
                json = $.parseJSON(data);
                success(json.data);
            });
        },

        list_svn: function(success){
            $.get("/list_svn", function(data){
                json = $.parseJSON(data);
                success(json.data);
            });
        },

        add: function(svnpaht, mail, success){
            $.ajax({
                type: 'POST',
                url: '/add',
                data: JSON.stringify ({"svnPath": svnpaht, "mail": mail}),
                success: function(data) {
                    json = $.parseJSON(data);
                    success(json);
                },
                contentType: "application/json",
                dataType: 'json'
            });
        },

        delete: function(id, success){
            $.ajax({
                type: 'POST',
                url: '/delete',
                data: JSON.stringify ({"id": id}),
                success: function(data) {
                    json = $.parseJSON(data);
                    success(json);
                },
                contentType: "application/json",
                dataType: 'json'
            });
        }
    }

    return _export;
};

var svnmonitor = SVNMonitor();

function renewList(){
    svnmonitor.list(function(data){
        var table_row = $(".table_row");

        if(0 != table_row.length)
            table_row.remove();

        var table_tr = $("#svn_list_table tr:last");

        for(key in data){
            item = data[key];
            table_tr.after("<tr class='table_row'><td>" + item.id + "</td>" +
                                                "<td>" + item.svnpath + "</td>" +
                                                "<td>" + item.mail + "</td>" +
                                                "<td><a href='#' onclick=del('" + item.id + "');>delete</a></td></tr>" );

            console.info($("#svn_list_table tr:last"));
        }
    });
}

function del(id){
    svnmonitor.delete(id, function(data){
        renewList();
    });
    return false;
}

function set_svn_list(){
    svnmonitor.list_svn(function(data){
        $.each(data, function(key, value) {
            $('#svnpath')
                .append($("<option></option>")
                .attr("id", value.id)
                .text(value.path));
        });
    });
}

$(function(){
    set_svn_list();
    renewList();

    $("#addsvn").click(function(){
        svnpath = $("#svnpath").val();
        mail = $("#mail").val();

        console.log(svnpath);
        console.log(mail);

        patterns_email = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
        if(false == patterns_email.test(mail))
            return false;

        svnmonitor.add(svnpath, mail, function(data){
            renewList();
        });

        return false;
    });
});