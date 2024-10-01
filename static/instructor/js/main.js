document.getElementById('profileDropdown').addEventListener('click', function() {
    var myDropdown = new bootstrap.Dropdown(this);
    myDropdown.toggle();
  });

// Create Assesment JS
document.addEventListener('DOMContentLoaded', function() {
  const correctAnswer = document.getElementById('id_correct_answer');
  const optionA = document.getElementById('id_option_a');
  const optionB = document.getElementById('id_option_b');
  const optionC = document.getElementById('id_option_c');
  const optionD = document.getElementById('id_option_d');

  function disableSelectedOption() {
    [optionA, optionB, optionC, optionD].forEach(option => {
        option.disabled = false;  // Re-enable all options
    });
    
    // Disable the selected correct answer in other fields
    const selectedOption = correctAnswer.value;
    if (selectedOption === 'A') optionA.disabled = true;
    if (selectedOption === 'B') optionB.disabled = true;
    if (selectedOption === 'C') optionC.disabled = true;
    if (selectedOption === 'D') optionD.disabled = true;
  }

  correctAnswer.addEventListener('change', disableSelectedOption);
});