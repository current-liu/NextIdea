
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
        }
    })
}

function str_to_table(){
    var str=$('#s1').val();
    console.log(str)
    $.ajax({
        url:schema_url+'/str_to_table',
        type:'GET',
        data:{"str":str},
        dataTpye:"json",
        success:function(res){
            var data = res
            console.log(data)
            console.log(data.length)
            console.log(data[0])
            for (var i=0; i<data.length; i++){

                tr = gen_tr(data[i])
            }


        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
        }
    })
}

function gen_tr(d){
    console.log("function gen_tr")
    console.log(d)

}





