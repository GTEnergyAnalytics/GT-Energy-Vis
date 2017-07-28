
// create color scale
col1 = '#00AEEF'
col2 = '#7a0019'
var color = d3.scaleLinear().domain([0,505.999143376]).range([col1,col2])

// d3.tip not currently working but could be added
// tip = d3.tip().html(function(d) { return 2; });
// console.log(tip)

// creating svg and g elements
var svg = d3.select("svg"),
    margin = {top: 80, right: 20, bottom: 30, left: 0},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom,
    g = svg.append("g").attr("transform", "translate(" + margin.left + "," + 0 + ")");
prev = 0

// bar height scale
var y = d3.scaleLinear()
    .domain([0, 1000000]).range([0, 500]);

// called to update static color
function updateColor() {
	$.getJSON('../../_calculate_hist', {
        datetime: $('input[name="datetime"]').val(),
        num_classes: $('input[name="num.classes"]').val(),
        temp: $('input[name="temp"]').val(),
        num_students: $('input[name="num_students"]').val()
    }, function(data) {
    	console.log(data.success, data.prediction);
        $('#Clough').attr('fill', color(data.truth))
        $('#Clough').attr('stroke', color(data.prediction))
        g.append('text')
            .text('Historical: ' + data.truth + ' kW h')
            .attr('x', -200)
            .attr('y', 100)
        g.append('text')
            .text('Prediction: ' + data.prediction + ' kW h')
            .attr('x', -200)
            .attr('y', 130)

    });
    console.log('sent')
    
  return false
}

// called to update bar cahrt
function updateTimePlot() {
    $.getJSON('../../_time_series', {
        num_classes: $('input[name="num.classes"]').val(),
        temp: $('input[name="temp"]').val(),
        num_students: $('input[name="num_students"]').val()
        // time: $('input[name="time"]').val()
    }, function(data) {
        // $("#result").text(data.result);
        console.log(data.success, data.prediction, data.months);
        // $('#Clough').attr('fill', x(data.truth))
        // $('#Clough').attr('stroke', x(data.prediction))
        var keys = data.months;
        dataBar = [data.truth, data.prediction]
        g.selectAll('*').remove()
        sum = 0
        for(i = 0; i < data.prediction.length; i++) {
            //iterate through data points and add bars (and month labels)
            g.append('rect')
                .attr('x' ,i * 50 + 60)
                .attr('y', 400 - y(data.prediction[i]))
                .attr('width', 40)
                .attr('height', y(data.prediction[i]))
                .attr('fill', "#1e90ff")
                // .on('mouseover', tip.show)
                // .on('mouseout', tip.hide)

            g.append('text')
                .attr('x' ,i * 50 + 65)
                .attr('y', 420)
                .text(data.months[i].substring(0,3))

            sum += data.prediction[i]
        }

        for (i = 0; i < 10; i++) {
            //iterate through step labels for energy consumptions
            g.append('text')
                .attr('x' ,0)
                .attr('y', 400-y(i*100000))
                .text(i*100000)
        }

        //add headers
        g.append('text')
            .attr('x', -20)
            .attr('y', 350)
            .text('Power Consumption (kW h)')
            .attr('transform', 'rotate(-90, -20, 350)')
        
        //alert difference from last calculation and set variable before next calculation
        alert('Total Power Expenditure: ' + sum + 'kW. This is a ' + (sum - prev) + "kW difference from your last calculation.");
        prev = sum
      });
}



// old data retrieval code (now done in app.py)
// csvStr = ''
// energyArr = null
// console.log('static/data/energy_hourly.csv');
// $.ajax({
//     type: "GET",
//     url: 'static/data/energy_hourly.csv',
//     dataType: "text",
//     success: function(data) {
//     	csvStr = data;
//     	energyArr = d3.csvParse(csvStr)
//     	console.log(energyArr[1]['power'])
//     }
// });

// old color update function
function sliderUpdate(vals) {

	energy = +(energyArr[mySlider.bootstrapSlider('getValue')]['power'])
	console.log(energy)
	finalColor = color(energy)
}


// Instantiate a slider
// var mySlider = $("input.slider").bootstrapSlider();
// mySlider.on('change', function(ev) {
// 	sliderUpdate(ev);
// })