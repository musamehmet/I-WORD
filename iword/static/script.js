document.getElementById("wordInput").addEventListener("input", function () {
    var inputValue = this.value.trim(); 
    if (inputValue.length < 1) {
        this.setCustomValidity("You must enter at least 1 character.");
    } else {
        this.setCustomValidity("");
    }
});


function toggleProfileHover() {
    var profileHover = document.querySelector(".profile-hover");

    if (profileHover.style.display === "block") {
      profileHover.style.display = "none";
    } else {
      profileHover.style.display = "block";
    }
  }

  document.addEventListener("click", function(event) {
    var profileHover = document.querySelector(".profile-hover");
    var profileImage = document.getElementById("profileImage");

    if (event.target !== profileHover && event.target !== profileImage) {
      profileHover.style.display = "none";
    }
  });


window.onload = function () {
 
  typeFinder();

  function typeFinder(){
    var elements = document.getElementsByName("wordtype");
    for (var i = 0; i < elements.length; i++) {
      var content = elements[i].textContent;
     
      switch (content) {
          case '1':
              elements[i].textContent = 'Noun';
              break;
          case '2':
              elements[i].textContent = 'Verb';
              break;
          case '3':
              elements[i].textContent = 'Adjectives';
              break;
          case '4':
              elements[i].textContent = 'Preverb';
              break;
          default:
              break;
      }
  }  
  }

  typeSelectFinder();


  function typeSelectFinder(){
    var select = document.getElementById("worddetailtype"); // "wordtypeSelect" id'sine sahip <select> öğesini seç
            var options = select.getElementsByTagName("option"); // <select> öğesinin seçeneklerini al

            for (var i = 0; i < options.length; i++) {
                var content = options[i].value; // Seçeneğin değerini al
                // Değerlere göre değişiklik yap
                switch (content) {
                    case '1':
                        options[i].textContent = 'Noun';
                        break;
                    case '2':
                        options[i].textContent = 'Verb';
                        break;
                    case '3':
                        options[i].textContent = 'Adjectives';
                        break;
                    case '4':
                        options[i].textContent = 'Preverb';
                        break;
                    default:
                        // Değer 1, 2, 3 veya 4 değilse değişiklik yapma
                        break;
                }
            }
  }

  pronFinder();

  function pronFinder(){
    var elements = document.getElementsByName("prontypedetail");
    for (var i = 0; i < elements.length; i++) {
      var content = elements[i].textContent;
     
      switch (content) {
          case '1':
              elements[i].textContent = 'EN';
              break;
          case '2':
              elements[i].textContent = 'US';
              break;
          default:
              break;
      }
  }  
  }

  pronSelectFinder();


  function pronSelectFinder(){
    var select = document.getElementById("worddetailpron"); // "wordtypeSelect" id'sine sahip <select> öğesini seç
            var options = select.getElementsByTagName("option"); // <select> öğesinin seçeneklerini al

            for (var i = 0; i < options.length; i++) {
                var content = options[i].value; // Seçeneğin değerini al
                // Değerlere göre değişiklik yap
                switch (content) {
                    case '1':
                        options[i].textContent = 'EN';
                        break;
                    case '2':
                        options[i].textContent = 'US';
                        break;
                    default:
                        // Değer 1, 2, 3 veya 4 değilse değişiklik yapma
                        break;
                }
            }
  }  
};



