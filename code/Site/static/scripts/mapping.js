// Copyright (c) 2017 Jonathan Bassen, Stanford University
local_uri
= "/" + page_data["platform"]
+ "/" + encodeURIComponent(page_data["course_name"])
+ "/" + encodeURIComponent(page_data["mapping_name"])

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
    .style("display", "block")
    .style("margin", "0px auto 0px")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "16px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("&#10095;&nbsp;&nbsp;" + page_data["mapping_name"])

var content_title = content.append("div")
    .style("margin", "0px auto 20px")
    .style("padding", "0px 20px 0px 20px")
    .style("background-color", "#6C7A89")
    .style("color", "#ffffff")
    .style("font-weight", "100")
    .style("font-size", "24px")
    .style("line-height", "40px")
    .html("Course Modules")

var modules = content.append("div")
    .style("margin-bottom", "40px")
    .selectAll("div")
    .data(page_data["module_names"])
    .enter()
    .append("a")
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
        return d;
    })
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })
