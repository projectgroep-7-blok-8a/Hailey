!function () {
    var width = 960,
        height = 500;

    var x = d3.scaleLinear()
        .range([0, width]);

    var y = d3.scaleLinear()
        .range([0, height]);

    var color = d3.scaleOrdinal(d3.schemeCategory20c);

    var vis = d3.select('#icicle').append("svg")
        .attr("width", width)
        .attr("height", height)

    var partition = d3.partition()
        .size([width, height])
        .padding(0)
        .round(true);

    // Breadcrumb dimensions: width, height, spacing, width of tip/tail.
    var b = {
        w: 150, h: 30, s: 3, t: 10
    };

    var rect = vis.selectAll("rect");
    var fo = vis.selectAll("foreignObject");
    var totalSize = 0;

     var svg = d3.select("#vis").append("svg")
    //.text("rewrwr")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + (height / 2) + ")");

    d3.json("../../../HaileyBackEnd/icicle_results.json", function (error, root) {
        if (error) throw error;

        root = d3.hierarchy(d3.entries(root)[0],
            // This function is called for every block
            // d consists of a key and a value
            // The key is the name of the block
            // The value is either an object containing block objects or a value, which represents the block's size
            function (d) {
                return d3.entries(d.value)
            })
            .sum(function (d) {
                return d.value
            })
            .sort(function (a, b) {
                return b.value - a.value;
            });
        partition(root);

        //add breadcrumb
        initializeBreadcrumbTrail();
        var percentage = 100;
        var percentageString = percentage + "%";

        d3.select("#percentage")
            .text(percentageString);

        d3.select("#explanation")
            .style("visibility", "");

        var sequenceArray = root.ancestors().reverse();
        //sequenceArray.shift(); // remove root node from the array
        updateBreadcrumbs(sequenceArray, percentageString);

        rect = rect
            .data(root.descendants())
            .enter().append("rect")
            .attr("block_name", function (d) {
                //console.log(d.data.key)
                return d.data.key;
            })
            .attr("x", function (d) {
                return d.x0;
            })
            .attr("y", function (d) {
                return d.y0;
            })
            .attr("width", function (d) {
                return d.x1 - d.x0;
            })
            .attr("height", function (d) {
                return d.y1 - d.y0;
            })
            .attr("fill", function (d) {
                return color((d.children ? d : d.parent).data.key);
            })
            .on("click", clicked);

        fo = fo
            .data(root.descendants())
            .enter().append("foreignObject")
            .attr("x", function (d) {
                return d.x0;
            })
            .attr("y", function (d) {
                return d.y0;
            })
            .attr("width", function (d) {
                return d.x1 - d.x0;
            })
            .attr("height", function (d) {
                return d.y1 - d.y0;
            })
            .style("cursor", "pointer")
            .text(function (d) {
                return d.data.key
            })
            .on("click", clicked);

        //get total size from rect
        totalSize = rect.node().__data__.value;
    });

    async function clicked(d) {
        x.domain([d.x0, d.x1]);
        y.domain([d.y0, height]).range([d.depth ? 20 : 0, height]);

        rect.transition()
            .duration(750)
            .attr("x", function (d) {
                return x(d.x0);
            })
            .attr("y", function (d) {
                return y(d.y0);
            })
            .attr("width", function (d) {
                return x(d.x1) - x(d.x0);
            })
            .attr("height", function (d) {
                return y(d.y1) - y(d.y0);
            });

        fo.transition()
            .duration(750)
            .attr("x", function (d) {
                return x(d.x0);
            })
            .attr("y", function (d) {
                return y(d.y0);
            })
            .attr("width", function (d) {
                return x(d.x1 - d.x0);
            })
            .attr("height", function (d) {
                return y(d.y1 - d.y0);
            });

        // code to update the BreadcrumbTrail();
        var percentage = (100 * d.value / totalSize).toPrecision(3);
        var percentageString = percentage + "%";
        if (percentage < 0.1) {
            percentageString = "< 0.1%";
        }

        d3.select("#percentage")
            .text(percentageString);

        d3.select("#explanation")
            .style("visibility", "");

        var sequenceArray = d.ancestors().reverse();
        //sequenceArray.shift(); // remove root node from the array
        updateBreadcrumbs(sequenceArray, percentageString);
        var words = [];
        for (vo of sequenceArray){
            words.push(vo.data.key)
        }

        console.log(words);
        //words[2] = compound
        //words[1] = disease


        //words passing to python
        $(document).ready(function boxes(){
            $('#submit').click(function () {
                redirectPost('/resultaten',{words})

            });
        });
		
		//function to pass words in a form
        function redirectPost(url, data) {
            var form = document.createElement('form');
            document.body.appendChild(form);
            form.method = 'post';
            form.action = url;
            for (var name in data) {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = name;
                input.value = JSON.stringify(data);
                form.appendChild(input);
            }
            form.submit();
        }

        //var to pass words to html
        //document.getElementById('disease').innerHTML = words[1];
        //document.getElementById('compound').innerHTML = words[2];

        var iets = d3.selectAll("rect");
        //console.log(iets);
        // You have to call this multiple times. "Javascript", do I need to say more?
        removeTextBlocksNuke();


        await waitshuffle(); //Wait for 666 milliseconds before printing labels
        if (!(document.getElementById("endlabel").textContent === "100%")) {
            for (var rectangles of iets._groups) {
                for (var rectangle of rectangles) {
                    //console.log(rectangle);
                    var text = d3.select("#icicle").select("svg").append("text");
                    text.attr("x", function (d) {
                        var xloc = rectangle.getAttribute("x");
                        if (xloc < 0) {
                            xloc = -300;
                        }
                        return xloc;
                    }).attr("y", (parseFloat(rectangle.getAttribute("y")) + 20).toString()).text(function (d) {
                        return rectangle.getAttribute("block_name");
                    }).attr("class", "textlabell")
                }
            }
        }
    }
	
	//remove the labels in all the rects
    function removeTextBlocks(){
        for (texto of document.getElementsByClassName("textlabell")){
            texto.remove()
        }
    }
	
	//remove labels
    function removeTextBlocksNuke(){
        // Java Script being Java Script
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
        removeTextBlocks();
    }
    function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
	
	//wait for print labels
    async function waitshuffle() {
      console.log('Taking a break...');
      await sleep(666);
    }
    function initializeBreadcrumbTrail() {
        // Add the svg area.
        var trail = d3.select("#breadcrumb").append("svg")
            .attr("width", width)
            .attr("height", 50)
            .attr("id", "trail");
        // Add the label at the end, for the percentage.
        trail.append("text")
            .attr("id", "endlabel")
            .style("fill", "#000");

        // Make the breadcrumb trail visible, if it's hidden.
        d3.select("#trail")
            .style("visibility", "");
    }

    // Generate a string that describes the points of a breadcrumb polygon.
    function breadcrumbPoints(d, i) {
        var points = [];
        points.push("0,0");
        points.push(b.w + ",0");
        points.push(b.w + b.t + "," + (b.h / 2));
        points.push(b.w + "," + b.h);
        points.push("0," + b.h);
        if (i > 0) { // Leftmost breadcrumb; don't include 6th vertex.
            points.push(b.t + "," + (b.h / 2));
        }
        return points.join(" ");
    }

    // Update the breadcrumb trail to show the current sequence and percentage.
    function updateBreadcrumbs(nodeArray, percentageString) {

        // Data join; key function combines name and depth (= position in sequence).
        var trail = d3.select("#trail")
            .selectAll("g")
            .data(nodeArray, function (d) {
                return d.data.key + d.depth;
            });

        // Remove exiting nodes.
        trail.exit().remove();

        // Add breadcrumb and label for entering nodes.
        var entering = trail.enter().append("g");

        entering.append("polygon")
            .attr("points", breadcrumbPoints)
            .style("fill", function (d) {
                return color((d.children ? d : d.parent).data.key);
            });

        entering.append("text")
            .attr("x", (b.w + b.t) / 2)
            .attr("y", b.h / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .text(function (d) {
                return d.data.key;
            });

        // Merge enter and update selections; set position for all nodes.
        entering.merge(trail).attr("transform", function (d, i) {
            return "translate(" + i * (b.w + b.s) + ", 0)";
        });

        // Now move and update the percentage at the end of the breadcrumb
        d3.select("#trail").select("#endlabel")
            .attr("x", (nodeArray.length + 0.5) * (b.w + b.s))
            .attr("y", b.h / 2)
            .attr("dy", "0.35em")
            .attr("text-anchor", "middle")
            .text(percentageString);

    }

}();