function show_panel(panel_index)
{
    let panels = [document.getElementById("practice_panel"),
        document.getElementById("stats_panel"),
        document.getElementById("about_panel")];
    let buttons = [document.getElementById("practice_button"),
        document.getElementById("stats_button"),
        document.getElementById("about_button")];

    for (let i = 0; i < panels.length; i++)
    {
        if (i === panel_index)
        {
            panels[i].style.display = "flex";
            buttons[i].classList.add("selected");
        }
        else
        {
            panels[i].style.display = "none";
            buttons[i].classList.remove("selected");
        }
    }
    console.log("Showing panel " + panel_index);
}

function init()
{
    show_panel(0);
}