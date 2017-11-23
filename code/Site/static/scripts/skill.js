local_uri
= "/" + page_data["platform"]
+ "/" + encodeURIComponent(page_data["course_name"])
+ "/" + encodeURIComponent(page_data["mapping_name"])
+ "/" + encodeURIComponent(page_data["module_name"])
+ "/" + encodeURIComponent(page_data["objective_name"])
+ "/" + encodeURIComponent(page_data["skill_name"])

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
    .style("margin", "0px auto 0px")
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "20px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("/")

var module_name = content.append("a")
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
        + "/" + encodeURIComponent(page_data["module_name"])
    )
    .html(page_data["module_name"])
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var objective_name = content.append("a")
    .style("margin", "0px auto 0px")
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "20px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("/")

var objective_name = content.append("a")
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
        + "/" + encodeURIComponent(page_data["module_name"])
        + "/" + encodeURIComponent(page_data["objective_name"])
    )
    .html(page_data["objective_title"])
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var skill_name = content.append("a")
    .style("display", "block")
    .style("margin", "0px auto 0px")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "16px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("&#10095;&nbsp;&nbsp;" + page_data["skill_title"])

var content_title = content.append("div")
    .style("margin", "0px auto 20px")
    .style("padding", "0px 20px 0px 20px")
    .style("background-color", "#6C7A89")
    .style("color", "#ffffff")
    .style("font-weight", "100")
    .style("font-size", "24px")
    .style("line-height", "40px")
    .html("Questions Associated with this Skill (Grouped by Module)")

var modules = content.append("div")

var module = modules.selectAll("div")
    .style("margin-bottom", "40px")
    .data(page_data["module_names"])
    .enter()
    .append("div")

var module_name = module.append("a")
    .style("display", "block")
    .style("margin", "20px 0px 0px 20px")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#ffffff")
    .style("line-height", "40px")
    .style("font-size", "20px")
    .style("background-color", "#2C3E50")
    .style("text-decoration", "none")
    .html(function(d) {
        return d;
    })

var activity = module.append("div")
    .selectAll("div")
    .data(function(d){
        return page_data["m_to_a_data"][d];
    })
    .enter()
    .append("div")

var activity_text = activity.append("div")
    .style("margin", "20px 20px 0px 40px")
    .style("padding", "10px 20px 10px 20px")
    .style("background-color", "#DADFE1")
    .style("color", "#2C3E50")
    .style("line-height", "20px")
    .style("font-size", "16px")
    .style("text-decoration", "none")
    .html(function(d) {
        return d["text"];
    })

var activity_attempts = activity.append("div")
    .style("margin", "0px 20px 0px 40px")
    .style("padding", "10px 20px 10px 20px")
    .style("color", "#049372")
    .style("line-height", "16px")
    .style("font-size", "16px")
    .style("text-decoration", "none")
    .html(function(d) {
        n_attempted = d["attempted"]
        total = d["attempted"] + d["unattempted"]
        return "attempted by: " + n_attempted + " / " + total;
    })

var activity_first = activity.append("div")
    .style("margin", "0px 20px 0px 40px")
    .style("padding", "10px 20px 10px 20px")
    .style("color", "#049372")
    .style("line-height", "16px")
    .style("font-size", "16px")
    .style("text-decoration", "none")
    .html(function(d) {
        n_first = d["first_correct"]
        n_attempted = d["attempted"]
        return "correct on first attempt: " + n_first + " / " + n_attempted;
    })

var activity_last = activity.append("div")
    .style("margin", "0px 20px 0px 40px")
    .style("padding", "10px 20px 10px 20px")
    .style("color", "#049372")
    .style("line-height", "16px")
    .style("font-size", "16px")
    .style("text-decoration", "none")
    .html(function(d) {
        n_last = d["last_correct"]
        n_attempted = d["attempted"]
        return "correct on last attempt: " + n_last + " / " + n_attempted;
    })


