col1 = '#00AEEF'
col2 = '#7a0019'
var x = d3.scaleLinear().domain([0,505.999143376]).range([col1,col2])
// var x = d3.scaleLinear().domain([0,505.999143376]).range(['green','red'])


function updateColor() {
	$.getJSON('../../_calculate_hist', {
        datetime: $('input[name="datetime"]').val(),
        num_classes: $('input[name="num.classes"]').val(),
        temp: $('input[name="temp"]').val(),
        num_students: $('input[name="num_students"]').val()
        // time: $('input[name="time"]').val()
    }, function(data) {
    	// $("#result").text(data.result);
    	console.log(data.success, data.truth, data.prediction);
        $('#Clough').attr('fill', x(data.truth))
        $('#Clough').attr('stroke', x(data.prediction))
    });
    console.log('sent')
  return false;
}

function updateTimePlot() {
    $.getJSON('../../_time_series', {
        num_classes: $('input[name="num.classes"]').val(),
        temp: $('input[name="temp"]').val(),
        num_students: $('input[name="num_students"]').val()
        // time: $('input[name="time"]').val()
    }, function(data) {
        // $("#result").text(data.result);
        console.log(data.success, data.truth, data.prediction);
        // $('#Clough').attr('fill', x(data.truth))
        // $('#Clough').attr('stroke', x(data.prediction))
    });
    console.log('sent')
  return false;
}


csvStr = ''
energyArr = null
console.log('static/data/energy_hourly.csv');
$.ajax({
    type: "GET",
    url: 'static/data/energy_hourly.csv',
    // url: url_for('static', filename='data/energy_hoursly.csv')
    dataType: "text",
    success: function(data) {
    	csvStr = data;
    	energyArr = d3.csvParse(csvStr)
    	console.log(energyArr[1]['power'])
    }
});


function sliderUpdate(vals) {

	energy = +(energyArr[mySlider.bootstrapSlider('getValue')]['power'])
	console.log(energy)
	finalColor = x(energy)
}


// Instantiate a slider
// var mySlider = $("input.slider").bootstrapSlider();
// mySlider.on('change', function(ev) {
// 	sliderUpdate(ev);
// })