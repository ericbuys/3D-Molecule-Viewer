$(document).ready(
    function() {
        //Loads the Nav Bar
        $("#navbar-placeholder").load("navbar.html");

        //Loads the Periodic Table
        if($('#periodic-table').length){
            $.getJSON("elements.json", function(data){
                let elements = data.elements;
                let index = 0;
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

                //Click functionality for each element
                $(".cell").click( function() {
                    
                    $(this).toggleClass("current");
                    if($(this).hasClass("inactive")) {
                        $(".form.backdrop").fadeTo(200, 1);
                        $(".form.popup").css("display", "flex");
                        
                    } else {
                        $.post("/remove-element",
                            {
                                number: $(".current").children(".number").html(),
                            },
                            function() {
                                $(".current").toggleClass("inactive");
                                $(".current").toggleClass("active");
                                $(".current").toggleClass("current");
                            }
                        );
                    }  
                });
                
            });
            
            //Loading Elements from Database
            $.get("database-elements", function(data) {
                let db_elements = data.split(',');

                for(let i = 0; i < db_elements.length; i++) {
                    $('div.cell div.number').filter( function() {
                        return $(this).text() == db_elements[i];
                    }).parent().addClass('active').removeClass('inactive');
                }
            }

            );
        }

        $(".header-container").click(
            function() {
                $(this).next("div").animate({
                    height: "toggle",
                }, 500);
            }
            
        )
        
        //Form Handler for Canel Button
        $(".cancel").click(
            function() {
                $(".form.popup").css("display", "none");
                $(".current").toggleClass("current");
                $(".form.backdrop").fadeOut(200);
            }
        )
        
        //Form Handler for adding an element
        $("#add-element").click(
            function() {
                //Checking if a radius was inputted
                if($("#radius").val() == '') {
                    $(".radius").addClass("invalid-input");
                    
                    setTimeout(function () { 
                        $('.radius').removeClass('invalid-input');
                    }, 1000);
                } else {
                    //Calling the POST Request
                    $.post("/add-element",
                        {
                            number: $(".current").children(".number").html(),
                            symbol: $(".current").children(".symbol").html(),
                            name: $(".current").children(".name").html(),
                            radius: $("#radius").val(),
                            colour1: $("#colour1").val(),
                            colour2: $("#colour1").val(),
                            colour3: $("#colour1").val()
                        },
                        function() {
                            $(".form.popup").css("display", "none");
                            $(".current").toggleClass("inactive");
                            $(".current").toggleClass("active");
                            $(".current").toggleClass("current");
                            $(".form.backdrop").fadeOut(200);
                        }
                    );
                }

                
              }
        )
    }
);