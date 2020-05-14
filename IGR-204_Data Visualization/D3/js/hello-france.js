//alert("Hello, France!")
var margin = {top: 10, right: 50, bottom: 20, left: 15};

const w=700;
const h=700;
const r = 10;

const w_hist = 400 - margin.left - margin.right;
const h_hist =800 - margin.left - margin.right;

let dataset = [];

//---------------------------------------------create SVG element for the map-----------------------------------------
var svg= d3.select("#map")
           .append("svg")
              .attr("width",w + 4*margin.left + 2*margin.right)
              .attr("height",h + 2*margin.top + 4*margin.bottom)
              .append("g")
              .attr("transform", "translate("+margin.left+","+2*margin.bottom+")");

//------------------------------------set svg area for the population histogram---------------------------------------
let svg_hist_pop = d3.select("#hist_population")
                .append("svg")
                  .attr("width",w_hist + margin.left + 2*margin.right)
                  .attr("height",h_hist + margin.top + 2*margin.bottom)
                  .style("border", "2px solid black")
                  .append("g")
                        .attr("transform","translate(" + 3.5 * margin.left + "," + margin.top + ")");

//-------------------------------------set svg area for the density hisogram--------------------------------------------
let svg_hist_dens = d3.select("#hist_density")
                      .append("svg")
                        .attr("width", w_hist+ margin.left + margin.right)
                        .attr("height", h_hist+ margin.left + margin.right)
                        .style("border", "2px solid black")
                      .append("g")
                        .attr("transform","translate(" + 3 * margin.left + "," + margin.top + ")");

//-------------------------------------tooltip for the map--------------------------------------------------------------
let div_tooltip = d3.select("#map")
          .append("div")
            .attr("class","tooltip")
            .attr("color","red")
            .attr("fill-opacity","0.9")
//--------------------------------------colors for the map-------------------------------------------------------------
var color = d3.scaleLinear()
                .domain([0,3])
                .range(["blue","red"])
             
//---------------------------------------------data load-------------------------------------------------------------
d3.tsv("data/france.tsv")
  .row((d,i)=> {
      return {
        postalCode: +d["Postal Code"],
        inseeCode : +d.inseecode,
        place: d.place,
        longitude: +d.x,
        latitude: +d.y,
        population: +d.population,
        density: +d.density
      };
    })

  .get((error, rows) => {
    console.log("Loaded" + rows.length + " rows");
        //handle error or set up visualization here
    if (rows.length > 0) {
      console.log("First row: ", rows[0]);
      console.log("Last row:", rows[rows.length-1]);
      //error with NaN
      var rows = rows.filter((row) => (row.population != 0 ))
      var rows = rows.filter((row) => (!isNaN(row.longitude) && !isNaN(row.latitude) )); 
      dataset = rows;

      x = d3.scaleLinear()
            .domain(d3.extent(rows, (row) =>  row.longitude))
            .range([0, w]);

      y = d3.scaleLinear()
            .domain(d3.extent(rows, (row) => row.latitude))
            .range([h,0]);

     //population
     pop =  d3.scaleLinear()
                    .domain(d3.extent(rows, (row)=> row.population))
                    .range([1,r]);
      //density
      den = d3.scaleLinear()
                    .domain(d3.extent(rows, (row)=> 1+row.density))
                    .range([0,100]); 

      draw();
      add_axis();
      draw_hist_density();
      draw_hist_population();
        }  
  })

//--------------------------------------------------------------------------------------------------------------------
function draw() {
  svg.selectAll("circle")
    .data(dataset)
    .enter()
    .append("circle")
    .on("mouseover", handleMouseOver)
    .on("mouseout", handleMouseOut)
      .attr("r",(d) => pop(d.population))
      .attr("cx", (d) => x(d.longitude))
      .attr("cy", (d) => y(d.latitude))
      .attr("fill", (d)=> color(den(d.density)))
      .attr("fill-opacity", (d)=>den(d.density))
}

//--------------------------------------------------------------------------------------------------------------------
function add_axis(){
// x axis
svg.append("g")
         .attr("class","x axis")
         .attr("transform", "translate(0,"+h+")")
         .call(d3.axisBottom(x))

// y axis
svg.append("g")
   .attr("class","y axis")
    .attr("transform", "translate(0, "+y+")")
    .call(d3.axisRight(y));
}

//-----------------Draw function for density histogram---------------------------------------------------------------------------------------------------
// https://www.d3-graph-gallery.com/graph/histogram_binSize.html
// https://bl.ocks.org/d3noob/96b74d0bd6d11427dd797892551a103c

function draw_hist_density() {
  // X axis
  var x_hist = d3.scaleLinear()
      .domain([0, 5000])
      //.domain([0, d3.max(dataset, function(d) { return d.density; })])
      .range([0, w_hist]);

  svg_hist_dens.append("g")
      .attr("transform", "translate(0," + h_hist + ")")
      .call(d3.axisBottom(x_hist));

  // Create histogram
  function update(nBin){
    var histogram = d3.histogram()
                    .value((d) => d.density)
                    .domain(x_hist.domain())
                    .thresholds(x_hist.ticks(nBin))

  // Create bins
    var bins = histogram(dataset)

  // Y axis
    var y_hist = d3.scaleLinear()
                  .range([h_hist, 0])
                  .domain([0, d3.max(bins, (d) => d.length)])

  // Y axis legend
    svg_hist_dens.append("g")
                .attr("class", "y axis")
                .call(d3.axisLeft(y_hist));

  // Plot histogram
  svg_hist_dens.selectAll("rect")
    .data(bins)
    .enter()
    .append("rect")
      .merge(svg_hist_dens)
      .transition()
      .duration(1000)
      .attr("x", 1)
      .attr("transform", function(d) { return "translate(" + x_hist(d.x0) + "," + y_hist(d.length) + ")"; })
      .attr("width", function(d) { return x_hist(d.x1) - x_hist(d.x0); })
      .attr("height", function(d) { return h_hist - y_hist(d.length); })
      .style("fill", "red")

  svg_hist_dens.exit()
                .remove()
              }
update(20)
d3.select("#nBin").on("input", function(){
  update(+this.value);

})

};


//-----------------Draw function for population histogram---------------------------------------------------------------------------------------------------
// https://www.d3-graph-gallery.com/graph/histogram_binSize.html
// https://bl.ocks.org/d3noob/96b74d0bd6d11427dd797892551a103c


function draw_hist_population() {

  var x_hist = d3.scaleLinear()
      .domain([0, 20000])
      .range([0, w_hist]);

  var y_hist = d3.scaleLinear()
                  .range([h_hist, 0])
                  .domain([0, 30000]);

  // Create histogram
  var histogram = d3.histogram()
                    .value((d) => d.population)
                    .domain(x_hist.domain())
                    .thresholds(x_hist.ticks(10));

var bins = histogram(dataset);

  // Plot histogram
svg_hist_pop.selectAll("rect")
      .data(bins)
      .enter()
      .append("rect")
      .attr("class", "bar")
      .attr("x", 1)
      .attr("transform", function(d) { return "translate(" + x_hist(d.x0) + "," + y_hist(d.length) + ")"; })
      .attr("width", function(d) { return x_hist(d.x1) - x_hist(d.x0); })
      .attr("height", function(d) { return h_hist - y_hist(d.length); })
      .style("fill", "blue");

  svg_hist_pop.append("g")
      .attr("transform", "translate(0," + h_hist + ")")
      .call(d3.axisBottom(x_hist));

  svg_hist_pop.append("g")
      .call(d3.axisLeft(y_hist));

}


//--------------------------------------------------------------------------------------------------------------------
function handleMouseOver(d, i) {
    div_tooltip.transition()
        .duration(3000)

            div_tooltip.html("<br><br> Move your mouse over the map to get information <br> <b>Place : </b>" + d.place + "<br>"
                    + "<b>Postal code : </b>" + d.postalCode + "<br>"
                    + "<b>Population : </b>" + d.population + "<br>"
                    + "<b>Density : </b>" + d.density + "<br>")            
}

//--------------------------------------------------------------------------------------------------------------------
function handleMouseOut(d, i) {
  div_tooltip.transition()
         .duration(2000)
         div_tooltip.html("<br> Move your mouse over the map to get information <br>")
}