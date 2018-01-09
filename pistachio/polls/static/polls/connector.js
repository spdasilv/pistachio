$(document).ready(function() {
   $("#requestAjax").submit(function(event){
        $.ajax({
             type:"POST",
             url:"/requestAjax/",
             data: {
                        'input': [
                            {
                                "id": 0,
                                "lat": 43.648709,
                                "lon": -79.385913,
                                "w": 0,
                                "t": 0
                            },
                            {
                                "id": 1,
                                "lat": 43.6424537,
                                "lon": -79.3861234,
                                "w": 8,
                                "t": 120
                            }
                        ]
                    },
             success: function(){
                 $('#message').html("<h2>Request Successful!</h2>")
             }
        });
        return false;
   });
});