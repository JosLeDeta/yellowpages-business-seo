
var search_button = $('#search_button');
var task_completed = true;
var result_section = $('#result_section');
var ws = new WebSocket("ws://127.0.0.1:5869/");

ws.onmessage = function (event) {
    let res = JSON.parse(event.data);
    if (res.action == 'result')
    {
        res.data.forEach(business => {
            result_section.append(RasterItem(business));
        });
    }
    else if(res.action == 'set_score')
    {
        SetScoreValue(res.id, res.score);
    }
    else if(res.action == 'final_results')
    {
        result_section[0].innerHTML = '';
        res.data.forEach(business => {
            result_section.append(RasterItem(business));
            SetScoreValue(business.id, business.score);
        });
    }
}

search_button.on('click', () => {
    if(task_completed)
    {
        search_button[0].disabled = true;

        let category = $('#category_input')[0].value;
        let location = $('#location_input')[0].value;
        let pages = $('#pages_input')[0].value;
        ws.send(JSON.stringify({action: 'search', data: [category, location, pages]}));
    }
});

function RasterItem(item)
{
    var order = '?';
    if(item.order) order =  item.order;

    let template = "<div id=\"result-" + item.id + "\" class=\"result_item\">";
    template += "<h3 class=\"item_index\">" + order + "</h3>";
    template += "<div class=\"item_separator\"></div>";
    template += "<h3 class=\"item_name\">" + item.name + "</h3>";
    template += "<div class=\"item_separator\"></div>";
    template += "<h3 class=\"item_website\">" + item.website + "</h3>";
    template += "<div class=\"item_separator\"></div>";
    template += "<div class=\"score\">";
    template += "<div class=\"score_fill\"></div>";
    template += "<h4 class=\"score_value\">wait</h4>";
    template += "</div>";
    template += "<div class=\"item_separator\"></div>";
    template += "<div class=\"more_info\">";
    template += "<div></div>";
    template += "<div></div>";
    template += "<div></div>";
    template += "</div>";
    template += "</div>";

    return template;
}


function SetScoreValue(id, value)
{
    if (value > 100) value = 100;
    else if(value < 0) value = 0;
    var score_fill = $('#result-'+id+'>.score>.score_fill')[0];
    score_fill.style.width = value + '%';
    $('#result-'+id+'>.score>.score_value')[0].innerHTML = value;
    if (value < 40)
        score_fill.style.background = 'red';
    else if(value < 70)
        score_fill.style.background = 'orange';
    else if(value <= 100)
        score_fill.style.background = '#02e802';
}


