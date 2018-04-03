// Copyright (c) 2017 Jonathan Bassen, Stanford University
local_uri
= "/" + page_data["platform"]
+ "/" + encodeURIComponent(page_data["course_name"])
+ "/" + encodeURIComponent(page_data["mapping_name"])
+ "/" + encodeURIComponent(page_data["module_name"])

radius = 80
p = 20

var arc = d3.svg.arc()
    .outerRadius(radius)
    .innerRadius(0);

var label_arc = d3.svg.arc()
    .outerRadius(radius)
    .innerRadius(radius / 3);

var pie = d3.layout.pie()
    .value(function(d) {
        return d["count"];
    })
    .sort(null)

var body = d3.select("body")
    .style("margin", "0px")
    .style("padding", "0px")
    .style("width", "100%")
    .style("height", "90%")
    .style("font-weight", "100")

var nav_bar = body.append("div")
    .style("position", "fixed")
    .style("top", "0")
    .style("left", "0")
    .style("height", "40px")
    .style("line-height", "40px")
    .style("width", "100%")
    .style("background-color", "#ffffff")
    .style("z-index", "10")
    .style("border-bottom", "1px solid #cccccc")

var sign_out = nav_bar.append("a")
    .style("float", "right")
    .style("background-color", "#1E8BC3")
    .style("color", "#ffffff")
    .style("font-size", "16px")
    .style("padding-left", "20px")
    .style("padding-right", "20px")
    .style("border-left", "1px solid #cccccc")
    .style("text-decoration", "none")
    .attr("href", "/logout")
    .html("Sign Out")

var oars_name = nav_bar.append("a")
    .style("float", "left")
    .style("color", "#1E8BC3")
    .style("font-size", "30px")
    .style("padding-left", "20px")
    .style("padding-right", "20px")
    .style("text-decoration", "none")
    .attr("href", "/")
    .html("OARS")

var content = body.append("div")
    .style("width", "100%")
    .style("height", "100%")
    .style("margin-top", "40px")

var course_name = content.append("a")
    .style("margin", "40px auto 0px")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#1E8BC3")
    .style("font-weight", "100")
    .style("font-size", "16px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .attr("href", "/" + page_data["platform"] + "/" + encodeURIComponent(page_data["course_name"]))
    .html(page_data["course_name"])
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var mapping_name = content.append("a")
    .style("margin", "0px auto 0px")
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "20px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("/")

var mapping_name = content.append("a")
    .style("margin", "0px auto 0px")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#1E8BC3")
    .style("font-weight", "100")
    .style("font-size", "16px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .attr(
        "href",
        "/" + page_data["platform"]
        + "/" + encodeURIComponent(page_data["course_name"])
        + "/" + encodeURIComponent(page_data["mapping_name"])
    )
    .html(page_data["mapping_name"])
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var module_name = content.append("a")
    .style("display", "block")
    .style("margin", "0px auto 0px")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "16px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("&#10095;&nbsp;&nbsp;" + page_data["module_name"])

var content_title = content.append("div")
    .style("margin", "0px auto 20px")
    .style("padding", "0px 20px 0px 20px")
    .style("background-color", "#6C7A89")
    .style("color", "#ffffff")
    .style("font-weight", "100")
    .style("font-size", "24px")
    .style("line-height", "40px")
    .html("Learning Objectives in this Module")

var objectives = content.append("div")
.attr("class", "objectives")

var objective = objectives.selectAll("div")
.attr("class", "objective")
    .data(page_data["objective_names"])
    .enter()
    .append("div")

var objective_name = objective.append("a")
.attr("class", "objective_name")
    .style("display", "block")
    .style("margin", "0px auto")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#2C3E50")
    .style("line-height", "40px")
    .style("font-size", "20px")
    .style("text-decoration", "none")
    .attr("href", function(d) {
        return local_uri + "/" + encodeURIComponent(d);
    })
    .html(function(d) {
        console.log(d)
        console.log(page_data["objective_to_t"][d])
        return page_data["objective_to_t"][d];
    })
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var objective_vis = objective.append("div")
.attr("class", "objective_vis")


var objective_svg = objective_vis.append("svg")
.attr("class", "objective_svg")
    .attr("width", 2 * radius + 2 * p)
    .attr("height", 2 * radius + 2 * p)
    .style("display", "block")
    .append("g")
    .attr("transform", "translate(" + (radius + p) + "," + (radius + p) + ")")
    .selectAll("path")
    .data(function(d) {
        return pie([
            {count: page_data["objective_states"][d]["mastered"].length, color: "#26C281"},
            {count: page_data["objective_states"][d]["unmastered"].length, color: "#555555"},
        ]);
    })
    .enter()
    .append("path")
    .attr("d", arc)
    .attr("fill", function(d) {
        return d.data["color"];
    })

var objective_label = objective.append("div")
    .style("margin", "0px auto")
    .style("font-weight", "400")
    .style("padding", "10px 20px 40px 20px")
    .style("color", "#6C7A89")
    .style("line-height", "20px")
    .style("font-size", "16px")
    .html(function(d) {
        var mastered = page_data["objective_states"][d]["mastered"].length;
        var total = mastered + page_data["objective_states"][d]["unmastered"].length;
        return "mastered by: " + String(mastered) + " / " + String(total);
    })
