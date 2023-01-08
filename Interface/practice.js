let question_title_text_mapping = {
    "article": "Type the correct article.",
    "meaning": "Select the correct meaning.",
    "english_names": "Translate this word into English."
};

function practice_init()
{
    eel.python_log("Initializing practice...");
    let answer_input = document.getElementById("answer_input");
    answer_input.addEventListener("keydown", function(event){
        if (event.key === "Enter")
        {
            answer();
        }
    });
    eel.create_question()(set_new_question);
    eel.python_log("Practice initialized.");
}

function change_category(category)
{
    eel.python_log("Changing category to " + category + "...");
    let category_checkbox = document.getElementById("practice_category_" + category);
    let is_checked = category_checkbox.checked;
    eel.set_category(category, is_checked)();
}

function answer_response(is_correct)
{
    let incorrect_answer_text = document.getElementById("incorrect_answer_text");
    if (is_correct){
        eel.create_question()(set_new_question);
    }
    else{
        eel.python_log("Incorrect answer.");
        incorrect_answer_text.classList.remove("opacity_transition");
        incorrect_answer_text.style.opacity = "1";
        setTimeout(function(){
            incorrect_answer_text.classList.add("opacity_transition");
            incorrect_answer_text.style.opacity = "0";
        }, 300);
    }
}

function answer()
{
    eel.python_log("Answering...");
    let answer_input = document.getElementById("answer_input");
    let answer = answer_input.value;

    eel.answer({"answer_text": answer})(answer_response);
}

function answer_option(option_index)
{
    eel.answer({"answer_option": option_index})(answer_response);
}

eel.expose(set_new_question);
function set_new_question(question_content)
{
    let no_categories = (question_content==="no_categories");

    eel.python_log("Setting new question...");
    let practice_content_title_text = document.getElementById("practice_content_title_text");
    let practice_question_text = document.getElementById("practice_question_text");
    let answer_input = document.getElementById("answer_input");
    let input_answer_content = document.getElementById("input_answer_content");
    let options_answer_content = document.getElementById("options_answer_content");

    if (no_categories)
    {
        practice_content_title_text.innerHTML = "No categories selected.";
        practice_question_text.innerHTML = "Please select at least one category in the settings.";
        input_answer_content.style.display = "none";
        options_answer_content.style.display = "none";
        return;
    }

    answer_input.value = "";

    let question_type = question_content["type"]; // "article", "meaning", "english_names"

    practice_content_title_text.innerHTML = question_title_text_mapping[question_type];
    practice_question_text.innerHTML = question_content["questioned_content"];



    for (let i = 0; i < 4; i++)
    {
        let cur_option_button = document.getElementById("option_button_" + (i + 1));
        cur_option_button.innerHTML = question_content["possible_answers"][i];
    }

    let enable_input_mode = (question_type ==="article")
    input_answer_content.style.display = enable_input_mode ? "flex" : "none";
    options_answer_content.style.display = enable_input_mode ? "none" : "grid";
    eel.python_log("New question set.");
}