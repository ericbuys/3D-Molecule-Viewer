$(document).ready(
    function() {
        //Loads the Nav Bar
        $("#navbar-placeholder").load("navbar.html");

        //Loads the Periodic Table
        if($('#periodic-table').length){
            $.getJSON("elements.json", function(data){
                let elements = data.elements;
                let index = 0;
                let currRow = 0;
                let items = [];
                let extras = [];
                let extraRows = [];
                let extraRowsClass = ['row extras', 'row']
                let extraRowsIndex = 0;

                let emptyCell = '<div class="cell blank"></div>';

                $.each(elements, function() {
                    if(!(index > 55 && index < 70) && !(index > 87 && index < 102)) {
                        if(index == 1 || index == 4 || index == 12) {
                            let emptyCellCount;

                            if(index == 1) {
                                emptyCellCount = 16;
                            } else {
                                emptyCellCount = 10;
                            }

                            for(let i = 0; i < emptyCellCount; i++) {
                                items.push(emptyCell);
                            }
                        }

                        items.push(
                            '<div class="cell inactive">\n' + 
                            '   <div class="number">' + elements[index].number + '</div>\n' +
                            '   <div class="symbol">' + elements[index].symbol + '</div>\n' +
                            '   <div class="name">' + elements[index].name + '</div>\n' +
                            '</div>\n');
                    } else {
                        extras.push(
                            '<div class="cell inactive">\n' + 
                            '   <div class="number">' + elements[index].number + '</div>\n' +
                            '   <div class="symbol">' + elements[index].symbol + '</div>\n' +
                            '   <div class="name">' + elements[index].name + '</div>\n' +
                            '</div>\n');
                    }

                    index++;

                    if(index == 2 || index == 10 || index == 18 || index == 36 || index == 54 || index == 86 || index == 118) {
                        let row =   '<div class="row">\n' +
                                        items.join("") +
                                    '</div>\n';
                        $(row).appendTo("#periodic-table");
                        items = [];

                        currRow++;
                    } else if (extras.length == 14) {

                        extraRows[extraRowsIndex] = '<div class="' + extraRowsClass[extraRowsIndex] + '">\n' +
                                                        extras.join("") +
                                                    '</div>\n';
                        extras = [];
                        extraRowsIndex++;
                    }
                });
                $(extraRows[0]).appendTo("#periodic-table");
                $(extraRows[1]).appendTo("#periodic-table");

                $(".cell").click(
                    function() {
                        $(this).toggleClass("inactive");
                        $(this).toggleClass("active");
                    }
                );
            });
        }

        $(".header-container").click(
            function() {
                $(this).next("div").animate({
                    height: "toggle",
                }, 500);
            }
        )
    }
);