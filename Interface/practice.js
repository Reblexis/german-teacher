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
    answer_input.value = "";

    eel.answer({"answer_input": answer})(answer_response);
}

function set_new_question(question_content)
{
    let practice_content_title_text = document.getElementById("practice_content_title_text");
    let practice_question_text = document.getElementById("practice_question_text");
    let question_type = question_content["type"]; // "article", "meaning", "english_names"

    practice_content_title_text.innerHTML = question_title_text_mapping[question_type];
    practice_question_text.innerHTML = question_content["word_data"]["name"];
}