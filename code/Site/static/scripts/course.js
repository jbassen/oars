local_uri
= "/" + page_data["platform"]
+ "/" + encodeURIComponent(page_data["course_name"])

var bar_p = 20
var bar_h = 60
var vis_h = 4*bar_p + 3*bar_h
var vis_w = 1600

var n_learners = page_data['n_learners']

var x_step = 5;
if(n_learners > 10000){
    x_step = 1000;
} else if(n_learners > 1000){
    x_step = 500;
} else if(n_learners > 500) {
    x_step = 100;
} else if(n_learners > 250){
    x_step = 50;
} else if(n_learners > 100){
    x_step = 25;
} else if(n_learners > 50){
    x_step = 10;
}

var x_ticks = [];
for(var i=0; i<=n_learners + (2*x_step); i+=x_step) {
    x_ticks.push(i);
}

var learner_scale = d3.scale.linear()
    .range([ 2*bar_p, vis_w - (2*bar_p) ])
    .domain([ 0, n_learners + 2*x_step])

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
    .style("color", "#6C7A89")
    .style("font-weight", "100")
    .style("font-size", "16px")
    .style("line-height", "40px")
    .style("text-decoration", "none")
    .html("&#10095;&nbsp;&nbsp;" + page_data["course_name"])

var content_title = content.append("div")
    .style("margin", "0px auto 20px")
    .style("padding", "0px 20px 0px 20px")
    .style("background-color", "#6C7A89")
    .style("color", "#ffffff")
    .style("font-weight", "100")
    .style("font-size", "24px")
    .style("line-height", "40px")
    .html("Course Maps")

var mappings = content.append("div")
.attr("class", "mappings")

var mapping = mappings.selectAll("div")
.attr("class", "mapping")
    .data(page_data["mappings_data"])
    .enter()

var mapping_name = mapping.append("a")
.attr("class", "mapping_name")
    .style("display", "block")
    .style("margin", "0px auto")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#2C3E50")
    .style("line-height", "40px")
    .style("font-size", "20px")
    .style("text-decoration", "none")
    .attr("href", function(d) {
        return local_uri + "/" + encodeURIComponent(d["mapping_name"]);
    })
    .html(function(d) { return d["mapping_name"]; })
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var mapping_label = mapping.append("a")
.attr("class", "mapping_label")
    .style("display", "block")
    .style("margin", "0px auto")
    .style("padding", "0px 20px 0px 20px")
    .style("color", "#2C3E50")
    .style("line-height", "40px")
    .style("font-size", "16px")
    .style("text-decoration", "none")
    .html(function(d) {
        return "This course map indicates learners have recently been struggling with the following skills...";
    })


var skills = mapping.append("div")

var skill = skills.selectAll("div")
.attr("class", "skills")
    .data(function(d){return d["skills_data"];})
    .enter()
    .append("div")

var skill_label = skill.append("a")
    .style("margin", "0px auto")
    .style("font-weight", "400")
    .style("padding", "10px 20px 40px 40px")
    .style("color", "#6C7A89")
    .style("line-height", "20px")
    .style("font-size", "16px")
    .attr("href", function(d) {
        return local_uri + "/"
        + encodeURIComponent(d["mapping_name"]) + "/"
        + encodeURIComponent(d["module_name"]) + "/"
        + encodeURIComponent(d["objective_name"]) + "/"
        + encodeURIComponent(d["skill_name"]);
    })
    .html(function(d) {
        if (! d["skill_title"]) {
          return "";
        } else {
            return d["skill_title"];
        }
    })
    .on('mouseover', function(d){
        d3.select(this).style("text-decoration", "underline");
    })
    .on('mouseout', function(d){
        d3.select(this).style("text-decoration", "none");
    })

var skill_vis = skill.append("div")
    .attr("class", "mapping_vis")

var skill_svg = skill_vis.append("svg")
    .attr("width", vis_w + "px")
    .attr("height", vis_h + "px")
    .style("display", "block")
    .append("g")

var mastered_bar = skill_svg.append("rect")
    .attr("x", learner_scale(0))
    .attr("y", bar_p)
    .attr("height", bar_h)
    .attr("width", function(d){
        return learner_scale(d["skill_state"]["mastered"].length) - learner_scale(0);
    })
    .style("fill", "#26C281")

var mastered_label = skill_svg.append("text")
    .attr("x", learner_scale(0))
    .attr("y", bar_p + (bar_h/2))
    .attr("dy", ".5em")
    .attr("dx", ".5em")
    .style("fill", "#dddddd")
    .text(function(d){
        var mastered = d["skill_state"]["mastered"].length;
        return mastered + " mastered";
    });

var unmastered_bar = skill_svg.append("rect")
    .attr("x", learner_scale(0))
    .attr("y", bar_p + (bar_p + bar_h) )
    .attr("height", bar_h)
    .attr("width", function(d){
        return learner_scale(d["skill_state"]["unmastered"].length) - learner_scale(0);
    })
    .style("fill", "#E26A6A")

var unmastered_label = skill_svg.append("text")
    .attr("x", learner_scale(0))
    .attr("y", bar_p + (bar_p + bar_h) + (bar_h/2))
    .attr("dy", ".5em")
    .attr("dx", ".5em")
    .style("fill", "#dddddd")
    .text(function(d){
        var unmastered = d["skill_state"]["unmastered"].length;
        return unmastered + " unmastered";
    });

var unknown_bar = skill_svg.append("rect")
    .attr("x", learner_scale(0))
    .attr("y", bar_p + (2*(bar_p + bar_h)) )
    .attr("height", bar_h)
    .attr("width", function(d){
        return learner_scale(d["skill_state"]["unknown"].length) - learner_scale(0);
    })
    .style("fill", "#555555")

var unknown_label = skill_svg.append("text")
    .attr("x", learner_scale(0))
    .attr("y", bar_p + (2*(bar_p + bar_h)) + (bar_h/2))
    .attr("dy", ".5em")
    .attr("dx", ".5em")
    .style("fill", "#dddddd")
    .text(function(d){
        var unknown = d["skill_state"]["unknown"].length;
        return unknown + " with too few attempts to assess";
    });
