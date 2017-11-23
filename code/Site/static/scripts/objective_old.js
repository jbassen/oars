local_uri
= "/" + page_data["platform"]
+ "/" + encodeURIComponent(page_data["course_name"])
+ "/" + encodeURIComponent(page_data["mapping_name"])
+ "/" + encodeURIComponent(page_data["module_name"])
+ "/" + encodeURIComponent(page_data["objective_name"])

var bar_w = 12
var bar_p = 4

var vis_h = 480
var vis_w = 800

var n_learners = page_data["n_learners"] + (49 - (page_data["n_learners"] % 50))
var n_problems = 49;

var x_ticks = [];
for(var i=0; i<=n_problems; i+=5) {
    x_ticks.push(i);
}

var y_ticks = [];
for(var i=0; i<=n_learners; i+=50) {
    y_ticks.push(i);
}

var mastered_scale = d3.scale.linear()
    .range([ (vis_h / 2) - (bar_w / 2) - bar_p, bar_p ])
    .domain([ 0, n_learners ])

var unmastered_scale = d3.scale.linear()
    .range([ (vis_h / 2) + (bar_w / 2) + bar_p, vis_h - bar_p ])
    .domain([ 0, n_learners ])

var attempts_scale = d3.scale.linear()
    .range([(bar_w * 2) + (bar_p * 2), vis_w])
    .domain([0, n_problems])

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
    .style("display", "block")
    .style("margin", "0px auto 0px")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "16px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("&#10095;&nbsp;&nbsp;" + page_data["objective_title"])

var content_title = content.append("div")
    .style("margin", "0px auto 20px")
    .style("padding", "0px 20px 0px 20px")
    .style("background-color", "#6C7A89")
    .style("color", "#ffffff")
    .style("font-weight", "100")
    .style("font-size", "24px")
    .style("line-height", "40px")
    .html("Skills Required for this Learning Objective")

var skills = content.append("div")

var skill = skills.selectAll("div")
    .data(page_data["skill_names"])
    .enter()
    .append("div")

var skill_name = skill.append("a")
    .style("display", "block")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#2C3E50")
    .style("line-height", "40px")
    .style("font-size", "20px")
    .style("text-decoration", "none")
    .attr("href", function(d) {
        return local_uri + "/" + encodeURIComponent(d);
    })
    .html(function(d) {
        return page_data["skill_to_t"][d];
    })
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var skill_vis = skill.append("div")
    .style("background-color", "#2C3E50")

var skill_svg = skill_vis.append("svg")
    .attr("width", vis_w + "px")
    .attr("height", vis_h + "px")
    .style("display", "block")
    .append("g")

var mastered_bars = skill_svg.append("g")
    .selectAll("g")
    .data(function(d) {
        return page_data["skill_states"][d]["learned_attempts"];
    })
    .enter()
    .append("g")
    .attr("transform", function(d, i) {
        return "translate(" + attempts_scale(i) + "," + mastered_scale(d) + ")";
    })

var mastered_bar = mastered_bars.append("rect")
    .attr("width", bar_w)
    .attr("height", function(d){
        return mastered_scale(0) - mastered_scale(d);
    })
    .style("fill", "#26C281")

var unmastered_bars = skill_svg.append("g")
    .selectAll("g")
    .data(function(d) {
        return page_data["skill_states"][d]["unlearned_attempts"];
    })
    .enter()
    .append("g")
    .attr("transform", function(d, i) {
        return "translate(" + attempts_scale(i) + "," + unmastered_scale(0) + ")";
    })

var unmastered_bar = unmastered_bars.append("rect")
    .attr("width", bar_w)
    .attr("height", function(d){
        return unmastered_scale(d) - unmastered_scale(0);
    })
    .style("fill", "#E26A6A")

var attempts_ticks = skill_svg.append("g")
    .selectAll("g")
    .data(x_ticks)
    .enter()
    .append("text")
    .attr("x", function(d){ return attempts_scale(d) + (bar_w / 2); })
    .attr("y", vis_h / 2 )
    .attr("dy", ".4em")
    .attr("dx", "-.4em")
    .style("fill", "#ffffff")
    .text(function(d, i){
        if(i === x_ticks.length - 3) {
            return d + " (attempted questions)";
        } else if(i > x_ticks.length - 3) {
            return "";
        } else {
            return d;
        }
    });

var mastered_ticks = skill_svg.append("g")
    .selectAll("g")
    .data(y_ticks)
    .enter()
    .append("text")
    .attr("x", bar_w / 2)
    .attr("y", function(d){ return mastered_scale(d); } )
    .attr("dy", ".5em")
    .attr("dx", "0em")
    .style("fill", "#ffffff")
    .text(function(d, i){
        return (i === y_ticks.length - 1) ? ("(learners who HAVE DEMONSTRATED MASTERY of this skill)") : d;
    });

var unmastered_ticks = skill_svg.append("g")
    .selectAll("g")
    .data(y_ticks)
    .enter()
    .append("text")
    .attr("x", bar_w / 2)
    .attr("y", function(d){ return unmastered_scale(d); } )
    .attr("dy", ".5em")
    .attr("dx", "0em")
    .style("fill", "#ffffff")
    .text(function(d, i){
        return (i === y_ticks.length - 1) ? ("(learners who HAVE NOT DEMONSTRATED MASTERY of this skill)") : d;
    });

var skill_label = skill.append("div")
    .style("margin", "0px auto")
    .style("font-weight", "400")
    .style("padding", "10px 20px 40px 20px")
    .style("color", "#6C7A89")
    .style("line-height", "20px")
    .style("font-size", "16px")
    .html(function(d) {
        var mastered = page_data["skill_states"][d]["learned_attempts"].reduce(function(a,b){return a+b;}, 0);
        var total = mastered + page_data["skill_states"][d]["unlearned_attempts"].reduce(function(a,b){return a+b;}, 0);
        return "mastered by: " + String(mastered) + " / " + String(total) + "\n"
        + "  (requires at least 4 attempts)";
    })
