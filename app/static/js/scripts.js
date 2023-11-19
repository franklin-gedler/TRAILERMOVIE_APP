document.addEventListener("DOMContentLoaded", function () {
    const currentPage = window.location.pathname.split("/").pop();

    // Obtén todos los elementos de enlace en el menú
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    // Itera sobre los enlaces y agrega la clase 'active' al enlace correspondiente
    navLinks.forEach(function(link) {
        const linkPath = link.getAttribute('href').split("/").pop();

        if (linkPath === currentPage) {
            link.classList.add('active');
        }
    });
});

// Función para crear elementos de video
function createVideoElement(data, idTipo) {
    let total_average;
    const container = document.createElement("div");
    //container.className = isMovie ? "pelicula" : "serie";
    container.className = "d-flex flex-column align-items-center justify-content-center position-relative";
    container.id = idTipo;
    

    const playIconContainer = document.createElement("div");
    //playIconContainer.className = "play-icon-container";
    playIconContainer.className = "play-icon-container d-flex align-items-center justify-content-center position-absolute";
    playIconContainer.setAttribute("data-video", data.video);

    const playIcon = document.createElement("i");
    playIcon.className = "fas fa-play play-icon";

    playIconContainer.appendChild(playIcon);

    const img = document.createElement("img");
    //img.src = `{{ url_for('static', filename='image/${data.img}') }}`;
    img.src = data.img;
    img.alt = data.alt;
    //img.className = isMovie ? "pelicula-img" : "serie-img";
    img.className = "img-movie-serie";

    const tooltip = document.createElement("div");
    tooltip.className = "image-tooltip";
    //tooltip.id = data.alt

    const titleParagraph = document.createElement("h3");
    titleParagraph.textContent = data.alt;
    titleParagraph.style.fontWeight = "bold";
    titleParagraph.style.textAlign = "center";

    // Crear un elemento de salto de línea
    //const lineBreak = document.createElement("br");
    const detailsParagraph = document.createElement("p");
    detailsParagraph.textContent = data.details;

    tooltip.appendChild(titleParagraph);
    //tooltip.appendChild(lineBreak);
    tooltip.appendChild(detailsParagraph);

    container.appendChild(playIconContainer);
    container.appendChild(img);
    container.appendChild(tooltip);

    const nameElement = data.alt

    const ratingForm = document.createElement("form");
    ratingForm.id = nameElement;
    ratingForm.className = "rating-form";

    const ratingParagraph = document.createElement("p");
    ratingParagraph.className = "rating clasificacion";

    for (let i = 5; i >= 1; i--) {
        const starInput = document.createElement("input");
        starInput.id = `radio${idTipo}-${i}`;
        starInput.type = "radio";
        starInput.name = `estrellas-${idTipo}`;
        starInput.value = i;

        const starLabel = document.createElement("label");
        starLabel.htmlFor = `radio${idTipo}-${i}`;
        starLabel.textContent = "★";

        starInput.addEventListener("change", function () {
            const selectedValue = this.value;
            //const formId = ratingForm.id;
            //sendRatingData(formId, selectedValue);
            const formall = ratingForm;
            sendRatingData(formall, selectedValue);
        });

        ratingParagraph.appendChild(starInput);
        ratingParagraph.appendChild(starLabel);
    }


    // Crear un span para el texto "Ganas de verla: "
    const ganasDeVerlaSpan = document.createElement("span");
    ganasDeVerlaSpan.textContent = '!Ganas de verla!';
    ganasDeVerlaSpan.style.color = 'white'; // Establecer el color blanco
    ganasDeVerlaSpan.style.display = 'block';
    
    const averageValueSpan = document.createElement("span");
    averageValueSpan.style.color = 'yellow';
    //averageValueSpan.id = `${nameElement.replace(/\s+/g, '-')}-${idTipo}`;
    averageValueSpan.className = `total-rating-${idTipo}`;

    ratingForm.style.display = "none";
    ratingForm.appendChild(ganasDeVerlaSpan);
    ratingForm.appendChild(ratingParagraph);
    ratingForm.appendChild(averageValueSpan);
    container.appendChild(ratingForm);

    // Mostrar el formulario al pasar el ratón sobre la imagen
    container.addEventListener("mouseover", () => {
        ratingForm.style.display = "block";
    });

    // Ocultar el formulario al quitar el ratón de la imagen
    container.addEventListener("mouseleave", () => {
        ratingForm.style.display = "none";
    });

    fetch(`/rating?name=${encodeURIComponent(data.alt)}`)
    .then(response => response.json())
    .then(ratingData => {
        total_average = ratingData.total_average;
        averageValueSpan.textContent = `${total_average || "0"}`;
    })
    .catch(error => {
        console.error("Error al realizar la solicitud:", error);
    });

    return container;
}


function sendRatingData(formall, selectedStar) {
    //console.log("formulario:", formall);
    const totalRatingElements = formall.querySelectorAll('[class^="total-rating"]')[0];

    // Capturar el id del formulario
    const name_element = formall.id;

    // Configurar los datos a enviar
    const formData = new FormData();
    formData.append('name', name_element);
    formData.append('rating', selectedStar);

    // Configurar la solicitud a Flask
    fetch('/rating', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        //console.log(data.value)
       
        // Actualizar el contenido del elemento con el nuevo valor
        if (totalRatingElements) {
            totalRatingElements.textContent = String(data.value);
        }
        
    })
    .catch(error => {
        console.error("Error al enviar la solicitud de rating:", error);
    });
    
    
}

// Función para crear el bloque de video-popup
function createVideoPopup() {
    const videoPopup = document.createElement("div");
    videoPopup.id = "video-popup";
    videoPopup.className = "video-popup";

    const videoContainer = document.createElement("div");
    videoContainer.className = "video-container";

    const iframe = document.createElement("iframe");
    iframe.id = "video-iframe";
    iframe.width = "560";
    iframe.height = "315";
    iframe.src = ""; // Establece la fuente del iframe según tus necesidades
    iframe.title = "YouTube video player";
    iframe.frameBorder = "0";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;

    videoContainer.appendChild(iframe);

    const closeButton = document.createElement("div");
    closeButton.id = "close-button";
    closeButton.className = "close-button";

    const closeIcon = document.createElement("i");
    closeIcon.className = "fas fa-times";

    closeButton.appendChild(closeIcon);

    videoPopup.appendChild(videoContainer);
    videoPopup.appendChild(closeButton);

    return videoPopup;
}

function Video_Popup() {
    const playButtons = document.querySelectorAll(".play-icon-container");
    const videoPopup = document.getElementById("video-popup");
    const videoIframe = document.getElementById("video-iframe");
    const closeButton = document.getElementById("close-button");
    
    playButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const videoId = button.getAttribute("data-video");
            //console.log("Video ID:", videoId); // Agregar esto
            const videoSrc = `https://www.youtube.com/embed/${videoId}`;
            //console.log("Video Source:", videoSrc); // Agregar esto
            videoIframe.src = videoSrc;
            videoPopup.style.display = "flex";
        });
    });

    closeButton.addEventListener("click", function () {
        videoIframe.src = "";
        videoPopup.style.display = "none";
    });
}


// Función para generar el tooltip
function gen_tooltip() {
    const images = document.querySelectorAll(".img-movie-serie");

    images.forEach((img) => {
        img.addEventListener("mouseover", function (event) {
            const x = event.clientX;
            const y = event.clientY;

            const tooltip = img.nextElementSibling;

            tooltip.style.left = x + "px";
            tooltip.style.top = y + "px";

            tooltip.style.display = "block";
        });

        img.addEventListener("mouseout", function () {
            const tooltip = img.nextElementSibling;
            tooltip.style.display = "none";
        });
    });
}


// Inicio Bloque para manejar la búsqueda
function search(event) {
    event.preventDefault();

    var formData = new FormData(event.target);

    fetch('/search', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
    
        localStorage.setItem('searchData', JSON.stringify(data));

        window.location.href = '/resultsearch';

    })
    .catch(error => {
        console.error('Error al realizar la solicitud:', error);
    });
}


document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === '/resultsearch') {
        const searchResultsContainer = document.getElementById('search-results-container');
        const searchData = JSON.parse(localStorage.getItem('searchData'));

        if (searchData) {
            if (searchData.moviesData.length === 0 && searchData.seriesData.length === 0) {
                // Ambas listas están vacías, mostrar mensaje de no se encontraron datos de búsqueda
                const noResultsMessage = document.createElement('h2');
                noResultsMessage.className = 'd-flex justify-content-center text-white';
                noResultsMessage.textContent = 'No se encontraron datos de búsqueda';
                searchResultsContainer.appendChild(noResultsMessage);

                // Eliminar el h2 existente
                const resultsHeading = document.querySelector('.results-heading');
                if (resultsHeading) {
                    resultsHeading.remove();
                }
            } else {
                // Al menos una de las listas tiene datos, mostrar resultados
                handleSearchResults(searchData, searchResultsContainer);
            }
        } else {
            console.error('No se encontraron datos de búsqueda.');
        }
    }
});


function handleSearchResults(data, container) {
    
    var elementCounter = 1;
    data.moviesData.forEach((movieData) => {
        const movieElement = createVideoElement(movieData, "search-movie-" + elementCounter);
        container.appendChild(movieElement);
        elementCounter++;
    });

    var elementCounter = 1;
    data.seriesData.forEach((seriesData) => {
        const seriesElement = createVideoElement(seriesData, "search-serie-" + elementCounter);
        container.appendChild(seriesElement);
        elementCounter++;
    });

    document.body.appendChild(createVideoPopup());

    gen_tooltip();
    Video_Popup();
}
// Fin Bloque para manejar la búsqueda



// Inicio generacion contenidos pages inicio, peliculas, series
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el nombre de la página actual sin la extensión
    //console.log(window.location.pathname.split("/").pop());
    const currentPage = window.location.pathname.split("/").pop();

    if (['inicio', 'peliculas', 'series'].includes(currentPage)) {
        
        fetch(`/${currentPage}`, {
            method: 'POST'
        })
        .then(response => response.json())
        /*
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
        */
        .then(data => {
            if (currentPage === 'inicio') {

                const moviesContainer = document.getElementById('movies-container');
                const seriesContainer = document.getElementById('series-container');

                var elementCounter = 1;
                data.moviesData.forEach((movieData) => {
                    const movieElement = createVideoElement(movieData, "movie-" + elementCounter);
                    moviesContainer.appendChild(movieElement);
                    elementCounter++;
                });

                var elementCounter = 1;
                data.seriesData.forEach((seriesData) => {
                    const seriesElement = createVideoElement(seriesData, "serie-" + elementCounter);
                    seriesContainer.appendChild(seriesElement);
                    elementCounter++;
                });

                document.body.appendChild(createVideoPopup());

            } else if (currentPage === 'peliculas') {

                const moviesContainer = document.getElementById('movies-container');

                var elementCounter = 1;
                data.moviesData.forEach((movieData) => {
                    const movieElement = createVideoElement(movieData, "movie-" + elementCounter);
                    moviesContainer.appendChild(movieElement);
                    elementCounter++;
                });

                document.body.appendChild(createVideoPopup());

            } else if (currentPage === 'series') {

                const seriesContainer = document.getElementById('series-container');

                var elementCounter = 1;
                data.seriesData.forEach((seriesData) => {
                    const seriesElement = createVideoElement(seriesData, "serie-" + elementCounter);
                    seriesContainer.appendChild(seriesElement);
                    elementCounter++;
                });

                document.body.appendChild(createVideoPopup());
            }
            gen_tooltip();
            Video_Popup();
        })
        .catch(error => console.error('Error:', error));
        
    }
});
// FIN generacion content all pages

// Inicio de la función para controlar el comportamiento del footer
document.addEventListener("DOMContentLoaded", function () {
    
    const footer = document.querySelector('footer');

    // Variable para rastrear la posición anterior del scroll
    let previousScrollPosition = window.pageYOffset || document.documentElement.scrollTop;

    // Función para controlar el comportamiento del footer
    function handleFooterVisibility() {
        const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;

        // Verifica si el usuario ha hecho scroll hacia abajo
        if (currentScrollPosition > previousScrollPosition) {
            // Si es así, oculta el footer
            footer.classList.add('hidden-footer');
        } else {
            // Si el usuario está haciendo scroll hacia arriba, muestra el footer
            footer.classList.remove('hidden-footer');
        }

        // Actualiza la posición anterior del scroll
        previousScrollPosition = currentScrollPosition;
    }

    // Asocia la función al evento scroll
    window.addEventListener('scroll', handleFooterVisibility);
});
// Fin de la función para controlar el comportamiento del footer

