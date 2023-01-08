function update_statistics() {
    let accuracy_plot = document.getElementById("accuracy_plot");
    accuracy_plot.src = "Media/accuracy_plot.png?random";
}
function show_statistics() {
    eel.show_statistics()(update_statistics);
}