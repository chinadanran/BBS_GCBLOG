    var pop_back_id="";
        function pop(url,id) {
            pop_back_id=id;
            console.log(pop_back_id);
            window.open(url+"?pop=1",url+"?pop=1","width=600,height=400,top=100,left=100")
        }

    function pop_back_func(text,pk) {
        var $option=$("<option>"); //  <option></option>
        $option.html(text);
        $option.attr("value",pk);
        $option.attr("selected","selected");
        $("#"+pop_back_id).append($option)
    }