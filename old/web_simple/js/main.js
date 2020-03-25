"use strict";

function rand_id(index) {
  return Math.round(Math.random() * index.length);
}

function print_article() {
  d3.selectAll(".article_txt").remove();
  var canvas = d3.select("#canvas");
  d3.json("newsfuzz.json", function(json) {
    var idx = Object.keys(json.index);
    var i = rand_id(idx);
    canvas.append("p").classed("article_txt", true).text("Source name: " + json.source_name[idx[i]]);
    canvas.append("p").classed("article_txt", true).text("Date: " + json.article_publishedAt[idx[i]]);
    canvas.append("p").classed("article_txt", true).text("Article Title: " + json.article_title[idx[i]]);
    canvas.append("p").classed("article_txt", true).text("Article description: " + json.article_description[idx[i]]);
    canvas.append("p").classed("article_txt", true).text("Topic guess: " + json.topic[idx[i]]);
  })
}

d3.select("#show_random_article").on("click", print_article);
