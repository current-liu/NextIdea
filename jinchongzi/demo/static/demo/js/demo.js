
function fun(){
    var id = 1
    $.ajax({
        url:schema_url+'/ajax',
        type:'GET',
        data:{"id":id},
        dataTpye:"json",
        success:function(res){
            console.log(res)
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
            console.log(errorThrown);
        }
    })
}

function str_to_table(){
    var str=$('#s1').val();
    var tbody = $('#table_demo');
    console.log(str);
    console.log(tbody);

    $.ajax({
        url:schema_url+'/str_to_table',
        type:'GET',
        data:{"str":str},
        dataTpye:"json",
        success:function(res){
            var data = res;
            console.log(data);
            console.log(data.length);
            console.log(data[0]);
            var str = "";
            for (var i=0; i<data.length; i++){
                var tr = gen_tr(data[i]);
                str += "<tr>" + tr + "</tr>";
            }
            var table = '<table  border="1" cellpadding="4" cellspacing="0" >'
                        + str + '</table>'
            console.log(str);
            tbody.html(table);

        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
            console.log(errorThrown);
        }
    })
}



function gen_tr(l){
    var tr = "";
    for(var i=0; i<l.length; i++){
        tr += "<td>"+l[i]+"</td>";
    }
    return tr
}





