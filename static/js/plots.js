$('#chg_type').on('change',function(){
    $.ajax({
        url: "{% url 'chgtp' %}",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('chg_type').value

        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('bargraph', data );
        }
    });
})
