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

                $.each(elements, function() {
                    if(!(index >= 55 && index <= 70) && !(index >= 87 && index <= 102)) {
                        items.push(
                            '<div class="cell">\n' + 
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
                    }
                });
            
            });
        }
    }
);