$(document).ready(
    function() {

        function clearElementForm() {
            $("#radius").val('');
            $("#colour1").val('');
            $("#colour2").val('');
            $("#colour3").val('');
        }

        //Loads the Nav Bar
        $("#navbar-placeholder").load("navbar.html");

        if($("#molecule-placeholder").length) {
            $.get("/load-molecule", function(data) {
                data = $.parseHTML(data)
                $(data).appendTo("#molecule-placeholder")
            });
        }

        //Loads the Periodic Table
        if($('#periodic-table').length){
            $.getJSON("elements.json", function(data){
                let elements = data.elements;
                console.log(elements)
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
                                                    emptyCell + emptyCell + emptyCell +
                                                    extras.join("") + emptyCell +
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
            });
        }

        $("#molecule-list").on("click", ".mol.container", function() {
            $.post("/select-molecule",
                {
                    molecule_name: $(this).find(".mol.name")[0].textContent
                }, 
                function() {
                    window.location.href = "/viewer.html"
                }
            );
            
        });

        if($('#molecule-list').length) {
            
            $.get("database-molecules", function(data) {
                data = JSON.parse(data);
                let index  = 0;
                items = [];

                $.each(data, function() {
                    items.push(
                        '<div class="mol container">\n' + 
                        '   <div class="mol main sub-container">Name:' +
                        '       <span class="mol name">' + data[index].name + '</span>\n' +
                        '   </div>' +
                        '   <div class="mol sub-container">Num Atoms:' +
                        '       <span class="mol num-atoms">' + data[index].num_atoms + '</span>\n' +
                        '   </div>' +
                        '   <div class="mol sub-container">Num Bonds:' +
                        '       <span class="mol num-bonds">' + data[index].num_bonds + '</span>\n' +
                        '   </div>' +
                        '</div>\n');

                    index++;
                });

                $(items.join("")).appendTo("#molecule-list");
            });
        }

        $(".header.resizable").click(
            function() {
                $(this).parent().next("div").animate({
                    height: "toggle",
                }, 500);
            }   
        )
        
        //Form Handler for Canel Button
        $(".cancel").click(
            function() {
                $(".form.popup").css("display", "none");
                clearElementForm();
                $(".current").toggleClass("current");
                $(".form.backdrop").fadeOut(200);
            }
        )

        //Make Upload SDF Form Appear
        $('.header.upload').click( function() {
            $(".form.backdrop").fadeTo(200, 1);
            $(".form.popup").css("display", "flex");
        });

        //Form Handler for Uploading an SDF File
        $("#upload-molecule").click( function() {
            let sendPostRequest = true;

            //Checking if a file was uploaded
            if($("#sdf_file").val() == '') {
                sendPostRequest = false;
                $("#sdf_file").parent().addClass("invalid-input");

                setTimeout(function () { 
                    $("#sdf_file").parent().removeClass('invalid-input');
                }, 1000);
            }

            //Checking if a filename was inputted
            if($("#file_name").val() == '') {
                sendPostRequest = false;
                $("#file_name").parent().addClass("invalid-input");

                setTimeout(function () { 
                    $("#file_name").parent().removeClass('invalid-input');
                }, 1000);
            }

            if(sendPostRequest) {
                //Read in Contents from File
                const file = $("#sdf_file").prop('files')[0];
                const fileReader = new FileReader();
                fileReader.readAsText(file)

                //Sending Post Request
                fileReader.onload = function () {
                    $.post("/upload-sdf",
                        {
                            file_name: $("#file_name").val(),
                            file_contents: fileReader.result
                        },
                        function() {
                            alert("SDF File Uploaded Successfully");
                            
                            //Adding New Molecule to HTML Page
                            $.get("database-molecules", function(data) {
                                data = JSON.parse(data);
                                let index  = 0;
                                let newMoleculeEntry;
                                
                                //Looping through each molecule until the new one is found
                                $.each(data, function() {
                                    if(data[index].name == $("#file_name").val()) {
                                        newMoleculeEntry =  '<div class="mol container">\n' + 
                                                            '   <div class="mol main sub-container">Name:' +
                                                            '       <span class="mol name">' + data[index].name + '</span>\n' +
                                                            '   </div>' +
                                                            '   <div class="mol sub-container">Num Atoms:' +
                                                            '       <span class="mol num-atoms">' + data[index].num_atoms + '</span>\n' +
                                                            '   </div>' +
                                                            '   <div class="mol sub-container">Num Bonds:' +
                                                            '       <span class="mol num-bonds">' + data[index].num_bonds + '</span>\n' +
                                                            '   </div>' +
                                                            '</div>\n';
                                    }
                                    index++;
                                });
                                $(newMoleculeEntry).appendTo("#molecule-list");

                            })

                            $(".form.popup").css("display", "none");

                            $(".form.backdrop").fadeOut(200);
                        }
                    );
                }
            }
        });

        $(".rotate-form").submit(function(event) {
            let rollVal = $("#roll").val();
            let pitchVal = $("#pitch").val();
            let yawVal = $("#yaw").val();

            if($("#roll").val() == '') {
                rollVal = 0;
            }
            if($("#pitch").val() == '') {
                pitchVal = 0;
            }
            if($("#yaw").val() == '') {
                yawVal = 0;
            }

            console.log(rollVal)
            console.log(pitchVal)
            console.log(yawVal)

            $.post("/rotate-mol",
                {
                    roll: rollVal,
                    pitch: pitchVal,
                    yaw: yawVal
                },
                function(data) {
                    data = $.parseHTML(data)
                    $("#molecule-placeholder").children().remove()
                    $(data).appendTo($("#molecule-placeholder"))
                }
            )
            
            event.preventDefault();
        })
        
        //Form Handler for adding an element
        $("#add-element").click(
            function() {
                //Checking if a radius was inputted
                if($("#radius").val() == '' || parseInt($("#radius").val()) < 25 ||parseInt($("#radius").val()) > 100 ) {
                    $(".radius").addClass("invalid-input");
                    $('.tooltiptext').addClass("tooltip-view");
                    
                    setTimeout(function () { 
                        $('.radius').removeClass('invalid-input');
                        $('.tooltiptext').removeClass("tooltip-view");
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
                            clearElementForm();
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