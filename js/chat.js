function stringToDec(str){
    var val=[];
    for(var i = 0; i < str.length; i++)
        val.push(str.charCodeAt(i).toString(10));

    return val.join("_");
}
function decToString(str){
    var val="";
    console.log(typeof(str));
    var arr = String(str).split("_");
    for(var i = 0; i < arr.length; i++)
        val += String.fromCharCode(arr[i]);
    return val;
}
function NewChater(time,message) {
    var t=document.createElement("div");
    t.className="iot";
    t.innerHTML=time;
    var m=document.createElement("div");
    m.className="ioh";
    m.innerHTML=message;
    var c=document.createElement("div");
    c.className="ioc";
    c.append(t);
    c.append(m);
    $("#oc").append(c);
}
$(document).ready(function () {
    var iico = $("#iic");

    var send=undefined;
    var uid=0;
    var pool={};

    function _i() {
        iico.clear = function () {
            this.val("")
        };
        iico.getVal = function () {
            return this.val()
        };
        iico.bind("input propertychange", function () {
            var str=iico.getVal();
            if (str.length>24)
                iico.val(str.slice(0,str.length-1));
            var _1=str[str.length-1];
            if (_1===undefined)
                return;
            if (_1!=="\n")
                return;
            var _2=str.slice(0,str.length-1);
            send=_2;
            iico.clear();
        });
        $.get("/cgi/chat_server.py?uid="+uid+"&types=-1",function(result){
            uid=result;
        });
    }

    function Update() {
        var types=0;
        if (send!==undefined){
            types=1;
            var ts=stringToDec(send);
        }
        send=undefined;
        $.get("/cgi/chat_server.py?uid="+uid+"&types="+types+(types?("&send="+ts):''),function(result){
            var _0=JSON.parse(result);
            _0.forEach(function(item,index){
                if (pool[item["utc"]]!==undefined)
                    return;
                pool[item["utc"]]=item;
                NewChater(item["uid"],decToString(item["message"]));
            });
        });
    }
    _i();
    setInterval(Update,2000);
});
